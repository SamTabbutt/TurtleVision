#This file is to handle all deep learning development and analysis. It is currently in its first stage
#I need to bush up on my linear algebra before making this functional

import numpy as np
import mxnet as mx
from mxnet import nd, autograd, gluon
from mxnet.gluon.data.vision import transforms as trans
import pickle      #included in python 3
import base64      #included in python 3
from PIL import Image
import gc

from .models import Frame, tag


ctx = mx.gpu() if mx.test_utils.list_gpus() else mx.cpu()
data_ctx = ctx
model_ctx = ctx

batch_size = 10
num_inputs = 255
num_outputs = 10

class MLP(gluon.Block):
    def __init__(self, **kwargs):
        super(MLP, self).__init__(**kwargs)
        with self.name_scope():
            self.dense0 = gluon.nn.Dense(64)
            self.dense1 = gluon.nn.Dense(64)
            self.dense2 = gluon.nn.Dense(10)

    def forward(self, x):
        x = nd.relu(self.dense0(x))
        x = nd.relu(self.dense1(x))
        x = self.dense2(x)
        return x

#import dataset as list of Frame instances

#normalize dataset and organize into 
#list of tuples?

#adapted from https://gluon.mxnet.io/chapter04_convolutional-neural-networks/cnn-gluon.html

def model_predict(net,data):
	output = net(data.as_in_context(model_ctx))
	return nd.argmax(output, axis=1)

def transform(data, label):
		return nd.transpose(data.astype(np.float32), (2,0,1))/255, label.astype(np.float32)

def evaluate_accuracy(data_iterator, net):
	acc = mx.metric.Accuracy()
	for i, (data, label) in enumerate(data_iterator):
		data = data.as_in_context(model_ctx).reshape((-1,255))
		label = label.as_in_context(model_ctx)
		output = net(data)
		predictions = nd.argmax(output, axis=1)
		acc.update(preds=predictions, labels=label)
	return acc.get()[1]

class initiateModel():
	def __init__(self, anal_type):
		self.type=anal_type

	def createDataArray(self):
		gc.collect()
		#Change for modulation. Doing only for current configuration
		anal_type_frames = Frame.objects.all().filter(tag__tag_type=self.type)

		train_data =[]
		train_label =[]

		for frame in anal_type_frames:
			im = frame.imgData
			np_bytes = base64.b64decode(im)
			np_array = pickle.loads(np_bytes)

			image_out=nd.array(np_array)

			label = frame.tag.tag_num
			enter_label = nd.array([label])
			(image_out, label_out) = transform(image_out,enter_label)
			train_data.append(image_out)
			train_label.append(enter_label)
		train_data_set = gluon.data.ArrayDataset(train_data,train_label)
		data = gluon.data.DataLoader(train_data_set, batch_size, shuffle=False)
		return data


	def defineAndTrainModel(self, train_data):
		num_hidden = 64
		net = gluon.nn.Sequential()
		with net.name_scope():
			net.add(gluon.nn.Dense(num_hidden, activation="relu"))
			net.add(gluon.nn.Dense(num_hidden, activation="relu"))
			net.add(gluon.nn.Dense(num_outputs))

		net.collect_params().initialize(mx.init.Normal(sigma=.1), ctx=model_ctx)
		softmax_cross_entropy = gluon.loss.SoftmaxCrossEntropyLoss()
		trainer = gluon.Trainer(net.collect_params(), 'sgd', {'learning_rate': .01})
		epochs = 10
		smoothing_constant = .01

		for e in range(epochs):
			cumulative_loss = 0
			for i, (data, label) in enumerate(train_data):
				data = data.as_in_context(model_ctx).reshape((-1, 255))
				label = label.as_in_context(model_ctx)
				with autograd.record():
					output = net(data)
					loss = softmax_cross_entropy(output, label)
				loss.backward()
				trainer.step(data.shape[0])
				cumulative_loss += nd.sum(loss).asscalar()


			test_accuracy = evaluate_accuracy(test_data, net)
			train_accuracy = evaluate_accuracy(train_data, net)
			print("Epoch %s. Loss: %s, Train_acc %s" %(e, cumulative_loss/num_examples, train_accuracy))


#creating instances this way assuming that batching isn't as important when applying the model
#more updates. for now going to create  pseudo-code
class applyModel():
	def __init__(self, anal_type, ses):
		self.type = anal_type
		delf.session = ses

	def fillSessionSeconds(self):
		return