import numpy as np
import torch
import torch.backends.cudnn as cudnn
import cv2
import yolact.yolact_module as yolact_module
from PIL import Image
from yolact.data import cfg

from yolact.utils.augmentations import FastBaseTransform
from yolact.yolact import Yolact

class Real_time_yolact():
    def __init__(self, cuda=True, detect=False):
        self.trained_model = 'yolact/weights/yolact_im400_53_7000.pth'
        self.config = 'yolact_base_config'

        if self.config is not None:
            yolact_module.set_cfg(self.config)

        if self.trained_model == 'interrupt':
            trained_model = yolact_module.SavePath.get_interrupt('weights/')
        elif self.trained_model == 'latest':
            trained_model = yolact_module.SavePath.get_latest('weights/', cfg.name)

        if self.config is None:
            model_path = yolact_module.SavePath.from_str(trained_model)
            # TODO: Bad practice? Probably want to do a name lookup instead.
            config = model_path.model_name + '_config'
            print('Config not specified. Parsed %s from the file name.\n' % config)
            yolact_module.set_cfg(config)

        if detect:
            cfg.eval_mask_branch = False

        with torch.no_grad():

            if cuda:
                cudnn.fastest = True
                torch.set_default_tensor_type('torch.cuda.FloatTensor')
            else:
                torch.set_default_tensor_type('torch.FloatTensor')

            self.net = Yolact()
            self.net.load_weights(self.trained_model)
            self.net.eval()

            if cuda:
                self.net = self.net.cuda()

            self.net.detect.use_fast_nms = True
            self.net.detect.use_cross_class_nms = False
            cfg.mask_proto_debug = False


    def segmentation(self, img):

        with torch.no_grad():
            h, w, _ = img.shape
            frame = torch.from_numpy(img).cuda().float()
            batch = FastBaseTransform()(frame.unsqueeze(0))
            preds = self.net(batch)
            classes, scores, boxes, masks = yolact_module.prep_display(5, preds, frame, 0.5, h, w, undo_transform=True,
                                                         class_color=False, mask_alpha=0.45, fps_str='')

            if not len(masks) :
                return np.zeros((img.shape[0], img.shape[1]))
            mask = masks[0]
            mask = mask.cpu().numpy()

            h,w = mask.shape
            filled_mask = np.zeros([h,w])

            contours = yolact_module.cv_contours(np.uint8(mask))
            C = len(contours)
            contours = sorted(contours, key=lambda x: cv2.contourArea(x))
            cv2.drawContours(filled_mask, contours, C-1, 255,thickness=-1) #Fills the biggest contour

            return filled_mask

    def process(self, image_1, image_2):
        # Get segmentation masks as numpy arrays
        mask_2 = self.segmentation(img=image_2)
        mask_2 = np.uint8(mask_2)

        return mask_2
