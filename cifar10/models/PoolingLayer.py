import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

class Pooling(nn.Module):
    def __init__(self, ks, method = 'max'):
        super(Pooling, self).__init__()
        self.ks = ks
        if (method == 'avg'):
            self.pooling = torch.nn.AvgPool1d(ks)
        else:
            self.pooling = torch.nn.MaxPool1d(ks)
        
 
    def forward(self, x, index):
        '''
        input shape: batch_size * n * in_feature;
        output shape: batch_size * n * out_feature;
        '''
        n, m = index.size();
        batch_size, _, hid = x.size();
        zeros = Variable(torch.zeros(batch_size, 1, hid).cuda());
        x = torch.cat((x,zeros), 1);
        
        index = index.view(n*m,)
        #print(x.size());
        #print(index.size());
        x = torch.index_select(x, 1, index);
        x = x.permute(0,2,1).contiguous();
        x = self.pooling(x);
        x = x.permute(0,2,1).contiguous();
        x = x.view(batch_size, n, -1);
        return x;
        