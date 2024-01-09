import numpy as np
import cv2 as cv
import os
from hsvfilter import HSVfilter
from check_codecs import get_installed_fourcc_codecs
from exceptions import WrongPathException, VideoReadError
#from blurcontrol import getKernel

class Masker:
    
    # constants
    TRACKBAR_WINDOW = "HSV Filter Trackbars"
    VIDEO_WINDOW = "Video Frame Viewer"
    MASK_WINDOW = "Masked Frame Viewer"
    PROCESSED_FRAME_WINDOW = "Processed Video Frame Viewer"


    # properties
    capture = None
    w = None
    h = None
    resolution = None
    fps = None
    length = None
    codec = None
    parent_dir = None
    name = None
    file_extension = None

    def __init__(self,video_path):
        #capture the input video
        try:
            self.capture = cv.VideoCapture(video_path)
            self.w = int(self.capture.get(cv.CAP_PROP_FRAME_WIDTH))
            self.h = int(self.capture.get(cv.CAP_PROP_FRAME_HEIGHT))
            self.resolution = (self.w,self.h)
            self.fps = self.capture.get(cv.CAP_PROP_FPS)
            self.length = int(self.capture.get(cv.CAP_PROP_FRAME_COUNT))
            self.codec = int(self.capture.get(cv.CAP_PROP_FOURCC))
            self.parent_dir = os.path.abspath(os.path.join(video_path, os.pardir)) 
            self.name = os.path.basename(video_path).split(".")[0]
            self.file_extension = os.path.basename(video_path).split(".")[-1]

            if not os.path.exists(video_path):
                raise WrongPathException
            if (self.capture.isOpened() == False):
                raise VideoReadError
        except WrongPathException:
            print('Video directory does not exist. Exiting...')
        except VideoReadError:
            print('Error reading video file. Please make sure the input file is a video. Exiting...')

    
    def init_control_gui(self):
        cv.namedWindow(self.TRACKBAR_WINDOW, cv.WINDOW_NORMAL)
        cv.resizeWindow(self.TRACKBAR_WINDOW, 400, 600)

        # required callback for the trackbars. we'll be using the getTrackbarPos() to do lookups
        # instead of the callback
        def nothing(position):
            pass
        
        # trackbars for HSV filtering. H: 0-179, S: 0-255, V: 0-255
        cv.createTrackbar('HMin', self.TRACKBAR_WINDOW, 0, 179, nothing)
        cv.createTrackbar('SMin', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VMin', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('HMax', self.TRACKBAR_WINDOW, 0, 179, nothing)
        cv.createTrackbar('SMax', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VMax', self.TRACKBAR_WINDOW, 0, 255, nothing)
        # default starting values for Min/Max trackbars
        cv.setTrackbarPos('HMin', self.TRACKBAR_WINDOW, 96)
        cv.setTrackbarPos('SMin', self.TRACKBAR_WINDOW, 169)
        cv.setTrackbarPos('VMin', self.TRACKBAR_WINDOW, 0)
        cv.setTrackbarPos('HMax', self.TRACKBAR_WINDOW, 179)
        cv.setTrackbarPos('SMax', self.TRACKBAR_WINDOW, 255)
        cv.setTrackbarPos('VMax', self.TRACKBAR_WINDOW, 255)

        # trackbars for increasing/decreasing saturation and value
        cv.createTrackbar('SAdd', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('SSub', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VAdd', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VSub', self.TRACKBAR_WINDOW, 0, 255, nothing)  

        # trackbar for Blur kernel size. Blur is applied before hsv filtering.
        cv.createTrackbar('Blur', self.TRACKBAR_WINDOW, 0, 20, nothing)
        # default starting value for Blur trackbar
        cv.setTrackbarPos('Blur', self.TRACKBAR_WINDOW, 10)

        # trackbar Activation of Clahe equalization before hsv filtering
        cv.createTrackbar('CLAHE', self.TRACKBAR_WINDOW, 0, 1, nothing)

        # trackbar for Close kernel size
        cv.createTrackbar('Close', self.TRACKBAR_WINDOW, 0, 20, nothing)

        # trackbar for object removal through contour filtering. Contour filtering is applied on the hsv mask.
        cv.createTrackbar('Object filter', self.TRACKBAR_WINDOW, 0, 25000, nothing)
        # default starting value for Object filter trackbar
        cv.setTrackbarPos('Object filter', self.TRACKBAR_WINDOW, 20000)

        # trackbar for hole removal through contour filtering. Contour filtering is applied on the hsv mask.
        cv.createTrackbar('Hole filter', self.TRACKBAR_WINDOW, 0, 25000, nothing)
        # default starting value for Hole filter trackbar
        cv.setTrackbarPos('Hole filter', self.TRACKBAR_WINDOW, 300)
          

    # returns an HSV filter object based on the control GUI trackbar positions
    def get_hsv_filter_from_controls (self):
        # Get current positions of trackbars for the HSV filter
        hsv_filter = HSVfilter()
        hsv_filter.hMin = cv.getTrackbarPos('HMin', self.TRACKBAR_WINDOW)
        hsv_filter.sMin = cv.getTrackbarPos('SMin', self.TRACKBAR_WINDOW)
        hsv_filter.vMin = cv.getTrackbarPos('VMin', self.TRACKBAR_WINDOW)
        hsv_filter.hMax = cv.getTrackbarPos('HMax', self.TRACKBAR_WINDOW)
        hsv_filter.sMax = cv.getTrackbarPos('SMax', self.TRACKBAR_WINDOW)
        hsv_filter.vMax = cv.getTrackbarPos('VMax', self.TRACKBAR_WINDOW)
        hsv_filter.sAdd = cv.getTrackbarPos('SAdd', self.TRACKBAR_WINDOW)
        hsv_filter.sSub = cv.getTrackbarPos('SSub', self.TRACKBAR_WINDOW)
        hsv_filter.vAdd = cv.getTrackbarPos('VAdd', self.TRACKBAR_WINDOW)
        hsv_filter.vSub = cv.getTrackbarPos('VSub', self.TRACKBAR_WINDOW)
        hsv_filter.clahe = cv.getTrackbarPos('CLAHE', self.TRACKBAR_WINDOW)
        hsv_filter.blur = cv.getTrackbarPos('Blur', self.TRACKBAR_WINDOW)
        hsv_filter.close = cv.getTrackbarPos('Close', self.TRACKBAR_WINDOW)
        hsv_filter.object = cv.getTrackbarPos('Object filter', self.TRACKBAR_WINDOW)
        hsv_filter.hole = cv.getTrackbarPos('Hole filter', self.TRACKBAR_WINDOW)

        return hsv_filter

    
    def get_kernel_size (self, trackbar_pos):
        # Get current positions of trackbars for blur/close kernel
        size_list = range(3,91,2)
        if trackbar_pos > 0:
            pos = trackbar_pos-1
            kernel_size = size_list[pos]
            return kernel_size

    
    # apply adjustments to HSV channel
    def shift_channel(self, c, amount):
        if amount > 0:
            lim = 255 - amount
            c[c >= lim] = 255
            c[c < lim] += amount
        elif amount < 0:
            amount = -amount
            lim = amount
            c[c <= lim] = 0
            c[c > lim] -= amount
        return c


    # applies HSV filter to the current frame
    def create_mask(self, frame, hsv_filter=None):
        
        # if no filter exists, create one from the values of the trackbars
        if not hsv_filter:
            hsv_filter = self.get_hsv_filter_from_controls()

        if hsv_filter.blur > 0:
            # Apply Gaussian blur
            blur_kernel_size = self.get_kernel_size(hsv_filter.blur)
            frame = cv.GaussianBlur(frame, (blur_kernel_size,blur_kernel_size), 0)
        
        # Apply CLAHE to frame before masking
        if hsv_filter.clahe:
            # Initialize CLAHE
            clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            # Split frame to R, G, B components and apply clahe to each component
            R, G, B = cv.split(frame)
            output1_R = clahe.apply(R)
            output1_G = clahe.apply(G)
            output1_B = clahe.apply(B)
            # Merge R, G, B components back to a single image frame
            frame = cv.merge((output1_R, output1_G, output1_B))

        # #Denoising test
        #frame = cv.fastNlMeansDenoisingColored(frame, None, 10, 10, 7, 7)

        # Convert BGR frame to HSV
        hsv_frame = cv.cvtColor(frame,cv.COLOR_BGR2HSV)
        
        h, s, v = cv.split(hsv_frame)
        s = self.shift_channel(s, hsv_filter.sAdd)
        s = self.shift_channel(s, -hsv_filter.sSub)
        v = self.shift_channel(v, hsv_filter.vAdd)
        v = self.shift_channel(v, -hsv_filter.sSub)
        hsv_frame = cv.merge([h, s, v])

        # HSV filter range thresholds
        lower = np.array([hsv_filter.hMin, hsv_filter.sMin, hsv_filter.vMin])
        upper = np.array([hsv_filter.hMax, hsv_filter.sMax, hsv_filter.vMax])

        # Generate the mask using the HSV thresholds
        mask = cv.inRange(hsv_frame, lower, upper)

        # Filter using contour area
        mask = self.apply_contour_filter(mask, hsv_filter.object, hsv_filter.hole)

        if hsv_filter.close > 0:
            # Remove small noise
            close_kernel_size = self.get_kernel_size(hsv_filter.close)
            mask = self.apply_close(mask, close_kernel_size)
        
        return mask, frame, hsv_filter
    

    def apply_contour_filter(self, frame, object_filter, hole_filter):
        
        # Apply contour filter to delete small objects
        cnts = cv.findContours(frame, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        # cnts = cnts[0]
        filtered_cnts = []
        for c in cnts:
            area = cv.contourArea(c)
            if area < object_filter:
                filtered_cnts.append(c)
        
        cv.drawContours(frame, filtered_cnts, -1, (0,0,0), -1)

        # Apply reverse contour filter to delete small holes
        frame = cv.bitwise_not(frame)
        cnts = cv.findContours(frame, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        # cnts = cnts[0]
        filtered_cnts = []
        for c in cnts:
            area = cv.contourArea(c)
            if area < hole_filter:
                filtered_cnts.append(c)
        
        cv.drawContours(frame, filtered_cnts, -1, (0,0,0), -1)

        # Restore clean mask
        frame = cv.bitwise_not(frame)

        return frame
    
    def apply_close(self, frame, kernel_size):

        # apply kernel to blur image
        kernel = np.ones((kernel_size,kernel_size),np.uint8)
        result = cv.morphologyEx(frame, cv.MORPH_CLOSE, kernel)

        return result
    
    
    def init_video_gui(self):
        self.init_control_gui()

        while self.capture.isOpened():
            ret, frame = self.capture.read()

            if not ret:
                print("Video Ended. Replaying from beginning ...")
                self.capture.set(cv.CAP_PROP_POS_FRAMES, 0)
                continue


            mask, procframe, hsv_filter = self.create_mask(frame)
            masked_frame = cv.bitwise_and(frame, frame, mask=mask)
            
            # initialize masked video image window
            cv.namedWindow(self.MASK_WINDOW,cv.WINDOW_NORMAL)
            cv.resizeWindow(self.MASK_WINDOW, 960,590) # resize window to half size (original is 1920x1080)
            cv.imshow(self.MASK_WINDOW, masked_frame) # show mask in window

            # initialize original video image window
            cv.namedWindow(self.VIDEO_WINDOW,cv.WINDOW_NORMAL)
            cv.resizeWindow(self.VIDEO_WINDOW, 960,590) # resize window to half size (original is 1920x1080)
            cv.imshow(self.VIDEO_WINDOW, frame) # show image in window

            # initialize processed video image window (blur, clahe etc..)
            cv.namedWindow(self.PROCESSED_FRAME_WINDOW,cv.WINDOW_NORMAL)
            cv.resizeWindow(self.PROCESSED_FRAME_WINDOW, 960,590) # resize window to half size (original is 1920x1080)
            cv.imshow(self.PROCESSED_FRAME_WINDOW, procframe) # show image in window

            if cv.waitKey(33) == ord('q'):
                cv.destroyAllWindows()
                break
            
        
        # Export HSV filter parameters from GUI to JSON
        hsv_filter.save_to_file(self.parent_dir)
        print(f'HSV filter parameters have been exported to the following directory:\n{self.parent_dir}\hsv_parameters_from_GUI.json \n')
        self.capture.release()

    def mask_and_export(self, outputfolder, hsvparams):

        outputname = self.name+'_masked'
        # Resolve output location of masked video
        if outputfolder:
            # Check if output folder exists, create it if it doesn't
            if not os.path.exists(outputfolder):
                os.makedirs(outputfolder)
            output = os.path.join(outputfolder,outputname) # output path for masked video
        else:
            # If no 'outputfolder' is given, create the output path from the 'inputfile' parent directory and 'outputname'
            output = os.path.join(self.parent_dir,outputname)
        
        hsv_filter = HSVfilter()

        hsv_filter.import_from_file(hsvparams)
        
        # Check available codecs
        installed_codecs = get_installed_fourcc_codecs()
        if self.codec in [cv.VideoWriter_fourcc(*i) for i in installed_codecs]:
            output = output+'.'+self.file_extension
            masked_video = cv.VideoWriter(output, self.codec, self.fps, self.resolution)
        else:
            print("Input video codec is not available. Default codec 'mp4v' (.mp4) will be used instead.")
            output = output+'.mp4'
            masked_video = cv.VideoWriter(output, cv.VideoWriter_fourcc(*'mp4v'), self.fps, self.resolution)

        print('Starting to proccess and mask video frames...')
        nframe = 0 # processed frame counter
        while self.capture.isOpened():
            ret, frame = self.capture.read() # extract frame
            
            if ret:
                nframe += 1
                mask,_,_ = self.create_mask(frame, hsv_filter) # compute mask  
                frame = cv.bitwise_and(frame, frame, mask=mask) # mask frame
                masked_video.write(frame)

                perc_complete = round((nframe/self.length)*100, 1) # % completion counter
                print(f'Masked {nframe} frames. Progress: {perc_complete}%. Ctrl+C to abort.', end='\r')
            else:
                if nframe==self.length:
                    print(f'\nVideo processing finished, masked a total of {nframe}.', end='\n')
                    print(f'Masked video saved in the following directory:\n {output}', end='\n')
                    break
                else:
                    print(f'\nFrame processing error on frame number {nframe}. Exiting ...')
                    break

        self.capture.release()
        masked_video.release()
