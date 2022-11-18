from .video_processing import *
from cv2.dnn import NMSBoxes
import torch


class Model:
    def __init__(self, weights, version, model_classes_file):
        self.model, self.name = self.load_model(weights, version)
        if model_classes_file != "":
            with open(model_classes_file) as stream:
                self.classes = yaml.safe_load(stream)['names']
        else:
            self.classes = list(range(100))

    def load_model(self, weights_path, model_version):
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        if weights_path == "default":
            print("Loading default weights")
            model = torch.hub.load('ultralytics/yolov5', model_version).to(device)
        else:
            print("Loading custom weights")
            model = torch.hub.load('ultralytics/yolov5', 'custom', path=weights_path).to(device)
        print("Model loaded")
        return model, model_version

    def __call__(self, img):
        return self.forward(img)

    def forward(self, img):
        """
        img: numpy array
        returns: [[x1, y1, x2, y2, confidence, classid]]
        """
        with torch.no_grad():
            results_device = self.model(img)  # batch of images
        results = results_device.pred[0].to('cpu').numpy()

        coords = results[:, :4]
        coords = coords.reshape(coords.shape[:-1] + (2, 2)).astype("int")
        coords = coords.tolist()
        prediction_scores = results[:, 4].round(3).tolist()
        prediction_classes = results[:, 5].astype("int").tolist()

        output_dict = {"detection_boxes": coords,
                       "detection_classes": prediction_classes,
                       "detection_scores": prediction_scores,
                       "num_detections": len(coords)}

        # [[x1, y1], [x2, y2]] to [x1, y1, x2, y2]
        if len(output_dict["detection_boxes"]) == 0:
            return []
        x = np.array(output_dict["detection_boxes"])
        x = x.reshape(len(x),-1)

        
        confs = np.expand_dims(np.array(output_dict['detection_scores']), 1)
        clss = np.expand_dims(np.array(output_dict['detection_classes']), 1)
        all_detections = np.hstack([x, confs, clss]).tolist()
        kept_detections = self.nms(all_detections)
        return kept_detections

    def xywh_convert(model_output):
        """
        Convert default yolo detection boxes to [x1, y1, x2, y2]
        """
        x = model_output['detection_boxes']
        x = np.array(x)
        y = np.zeros((x.shape[0], 4))
        y[:,:2] = x.mean(1)
        y[:,2] = x[:,1,0] - x[:,0,0]
        y[:,3] = x[:,1,1] - x[:,0,1]
        y = np.abs(y)
        return y


    def x1y1x2y2_to_xminyminwh(self, x):
        """
        [[x1, y1, x2, y2, conf, clss]] to [xmin, ymin, w, h], conf
        clss is optional. input can be of shape (len, x>=5)
        """
        y = np.array(x)[:,:5]
        out = y.copy()[:,:4]
        out[:,0] = y[:, [0,2]].min(1)
        out[:,1] = y[:, [1,3]].min(1)
        out[:,2] = np.abs(y[:,0] - y[:,2])
        out[:,3] = np.abs(y[:,1] - y[:,3])
        return out.astype("int").tolist(), y[:,4].tolist()

    def nms(self, bboxes, conf_threshold = 0.3, nms_threshold = 0.5):
        """
        bboxes: model output in [x1, y1, x2, y2, optional: (conf, clss)] format

        returns: kept bboxes in same format as input
        """
        
        if len(bboxes) < 2:
            return bboxes
        
        bboxes_xminymin, confs = self.x1y1x2y2_to_xminyminwh(bboxes)
        keep_idx = NMSBoxes(bboxes_xminymin, confs, conf_threshold, nms_threshold)
            
        return [bboxes[i] for i in keep_idx]