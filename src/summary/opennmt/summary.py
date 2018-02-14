#!/usr/bin/env python

from __future__ import division, unicode_literals
import os
from argparse import Namespace
import math
import codecs
import torch

from itertools import count

import onmt.io
import onmt.translate
import onmt
import onmt.ModelConstructor
import onmt.modules
import sys

opt = Namespace(alpha=0.0, attn_debug=False, batch_size=1, beam_size=10, beta=-0.0, data_type='text', dump_beam='', dynamic_dict=False, gpu=-1 , max_length=100, max_sent_length=None, min_length=0, model=os.path.dirname(os.path.abspath(__file__)) + '/../../../models/summorization/tmp__acc_55.92_ppl_5.70_e50.pt', n_best=1, output='pred.txt', replace_unk=True, report_bleu=False, report_rouge=False, sample_rate=16000, share_vocab=False, src=os.path.dirname(os.path.abspath(__file__)) + '/../../../data/src-test.txt', src_dir='', tgt=None, verbose=False, window='hamming', window_size=0.02, window_stride=0.01)

opt.cuda = opt.gpu > -1
if opt.cuda:
    torch.cuda.set_device(opt.gpu)

# Load the model.
fields, model, model_opt = \
    onmt.ModelConstructor.load_test_model(opt, {})

# Sort batch by decreasing lengths of sentence required by pytorch.
# sort=False means "Use dataset's sortkey instead of iterator's".
# Translator
scorer = onmt.translate.GNMTGlobalScorer(opt.alpha, opt.beta)
translator = onmt.translate.Translator(model, fields,
                                       beam_size=opt.beam_size,
                                       n_best=opt.n_best,
                                       global_scorer=scorer,
                                       max_length=opt.max_length,
                                       copy_attn=model_opt.copy_attn,
                                       cuda=opt.cuda,
                                       beam_trace=opt.dump_beam != "",
                                       min_length=opt.min_length)

def summorize(req):
    f = open('/tmp/mentorhack_data.tmp', 'w')
    f.write(req)
    f.close()
    data = onmt.io.build_dataset(fields, opt.data_type, '/tmp/mentorhack_data.tmp', opt.tgt, src_dir=opt.src_dir, sample_rate=opt.sample_rate, window_size=opt.window_size, window_stride=opt.window_stride, window=opt.window, use_filter_pred=False) 
    data_iter = onmt.io.OrderedIterator(dataset=data, device=opt.gpu, batch_size=opt.batch_size, train=False, sort=False, sort_within_batch=True, shuffle=False) 
    builder = onmt.translate.TranslationBuilder(data, translator.fields, opt.n_best, opt.replace_unk, opt.tgt)
    for batch in data_iter:
        batch_data = translator.translate_batch(batch, data)
        translations = builder.from_batch(batch_data)

        trans = translations[0]
        best_pred = " ".join(trans.pred_sents[0])
        return best_pred

if __name__ == "__main__":
    for req in sys.stdin:
        print(summorize(req))
