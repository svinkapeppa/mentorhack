#!/usr/bin/env python3

from __future__ import division, unicode_literals
import os
import argparse
import math
import codecs
import torch

from itertools import count

import summary.opennmt.onmt.io
import summary.opennmt.onmt.translate
import summary.opennmt.onmt
import summary.opennmt.onmt.ModelConstructor
import summary.opennmt.onmt.modules
import opts

parser = argparse.ArgumentParser(
    description='translate.py',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
opts.add_md_help_argument(parser)
opts.translate_opts(parser)

opt = parser.parse_args()

def main():
    dummy_parser = argparse.ArgumentParser(description='train.py')
    opts.model_opts(dummy_parser)
    dummy_opt = dummy_parser.parse_known_args([])[0]

    opt.cuda = opt.gpu > -1
    if opt.cuda:
        torch.cuda.set_device(opt.gpu)

    # Load the model.
    fields, model, model_opt = \
        onmt.ModelConstructor.load_test_model(opt, dummy_opt.__dict__)

    # File to write sentences to.
    #out_file = codecs.open(opt.output, 'w', 'utf-8')

    # Test data
    data = onmt.io.build_dataset(fields, 'text',
                                 opt.src, None,
                                 src_dir=opt.src_dir,
                                 sample_rate=opt.sample_rate,
                                 window_size=opt.window_size,
                                 window_stride=opt.window_stride,
                                 window=opt.window,
                                 use_filter_pred=False)
#data = TextDataset(fields, src_examples_iter, None,
#        num_src_feats, num_tgt_feats,
#        src_seq_length=0,
#        tgt_seq_length=0,
#        dynamic_dict=True,
#        use_filter_pred=False)

    # Sort batch by decreasing lengths of sentence required by pytorch.
    # sort=False means "Use dataset's sortkey instead of iterator's".
    data_iter = onmt.io.OrderedIterator(
        dataset=data, device=opt.gpu,
        batch_size=1, train=False, sort=False,
        sort_within_batch=True, shuffle=False)

    # Translator
    scorer = onmt.translate.GNMTGlobalScorer(opt.alpha, opt.beta)
    translator = onmt.translate.Translator(model, fields,
                                           beam_size=opt.beam_size,
                                           n_best=1,
                                           global_scorer=scorer,
                                           max_length=opt.max_length,
                                           copy_attn=model_opt.copy_attn,
                                           cuda=opt.cuda,
                                           beam_trace=opt.dump_beam != "",
                                           min_length=opt.min_length)
    builder = onmt.translate.TranslationBuilder(
        data, translator.fields,
        1, opt.replace_unk, opt.tgt)

    for batch in data_iter:
        batch_data = translator.translate_batch(batch, data)
        translations = builder.from_batch(batch_data)

        for trans in translations:
            print(" ".join(trans.pred_sents[0]))

if __name__ == "__main__":
    main()
