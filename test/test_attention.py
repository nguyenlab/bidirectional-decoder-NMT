"""
Here come the tests for attention types and their compatibility
"""

import unittest
import torch
import onmt

from torch.autograd import Variable


class TestAttention(unittest.TestCase):

    def test_masked_global_attention(self):
        source_lengths = torch.IntTensor([7, 3, 5, 2])
        illegal_weights_mask = torch.ByteTensor([
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 1, 1],
            [0, 0, 1, 1, 1, 1, 1]])

        batch_size = source_lengths.size(0)
        dim = 20

        context = Variable(torch.randn(batch_size, source_lengths.max(), dim))
        hidden = Variable(torch.randn(batch_size, dim))

        attn = onmt.modules.GlobalAttention(dim)

        _, alignments = attn(hidden, context, context_lengths=source_lengths)
        illegal_weights = alignments.masked_select(illegal_weights_mask)

        self.assertEqual(0.0, illegal_weights.data.sum())
