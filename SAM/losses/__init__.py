import torch
import torch.nn as nn
from .losses import CustormLoss
import numpy as np

AVAI_LOSS = {'ce': nn.CrossEntropyLoss, 'multi_label_soft_margin': nn.MultiLabelSoftMarginLoss,
             'test_custom': CustormLoss, 'mse': nn.MSELoss}


def get_losses(losses):
    loss_dict = {}
    for name in losses:
        assert name in AVAI_LOSS, print('{name} is not supported, please implement it first.'.format(name=name))
        if losses[name].params is not None:
            # loss_dict[name] = AVAI_LOSS[name](**losses[name].params)
            temp = np.array([0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.25, 0.5, 0.5, 0.5, 0.5, 0.5], dtype=np.float32)
            loss_dict[name] = nn.CrossEntropyLoss(ignore_index=0, weight=torch.from_numpy(temp).to('cuda:0'))
        else:
            loss_dict[name] = AVAI_LOSS[name]()

    return loss_dict


import torch.nn as nn
import torch.nn.functional as F
import torch


class FocalLoss(nn.Module):
    def __init__(self, alpha=1, gamma=0, size_average=True, ignore_index=255):
        super(FocalLoss, self).__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.ignore_index = ignore_index
        self.size_average = size_average

    def forward(self, inputs, targets):
        ce_loss = F.cross_entropy(
            inputs, targets, reduction='none', ignore_index=self.ignore_index)
        pt = torch.exp(-ce_loss)
        focal_loss = self.alpha * (1 - pt) ** self.gamma * ce_loss
        if self.size_average:
            return focal_loss.mean()
        else:
            return focal_loss.sum()
