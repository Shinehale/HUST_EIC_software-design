from src.lib.processors_noopenmdao import findFaceGetPulse
from src.lib.interface import plotXY, imshow, waitKey, destroyWindow
from cv2 import moveWindow
import argparse
import numpy as np
import datetime
import cv2, sys


class PulseDetect:
    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.w, self.h = 0, 0
        self.pressed = 0
        self.processor = findFaceGetPulse(bpm_limits=[50, 160],
                                          data_spike_limit=2500.,
                                          face_detector_smoothness=10.)
        self.bpm_plot = False
        self.plot_title = "Data display - raw signal (top) and PSD (bottom)"

        self.key_controls = {"s": self.toggle_search,
                             "d": self.toggle_display_plot,
                             "f": self.write_csv}

    def toggle_search(self):
        # state = self.processor.find_faces.toggle()
        state = self.processor.find_faces_toggle()
        print("face detection lock =", not state)

    def toggle_display_plot(self):
        if self.bpm_plot:
            print("bpm plot disabled")
            self.bpm_plot = False
            destroyWindow(self.plot_title)
        else:
            print("bpm plot enabled")
            if self.processor.find_faces:
                self.toggle_search()
            self.bpm_plot = True
            self.make_bpm_plot()
            moveWindow(self.plot_title, self.w, 0)

    def make_bpm_plot(self):
        """
        Creates and/or updates the data display
        """
        plotXY([[self.processor.times,
                 self.processor.samples],
                [self.processor.freqs,
                 self.processor.fft]],
               labels=[False, True],
               showmax=[False, "bpm"],
               label_ndigits=[0, 0],
               showmax_digits=[0, 1],
               skip=[3, 3],
               name=self.plot_title,
               bg=self.processor.slices[0])

    def write_csv(self):
        """
        Writes current data to a csv file
        """
        fn = './data/pulse/' + str(datetime.datetime.now())
        fn = fn.replace(":", "_").replace(".", "_")
        data = np.vstack((self.processor.times, self.processor.samples)).T
        np.savetxt(fn + ".csv", data, delimiter=',')
        print("Writing csv")

    def key_handler(self):
        self.pressed = waitKey(10) & 255  # wait for keypress for 10 ms
        if self.pressed == 27:  # exit program on 'esc'
            print("Exiting")
            self.cam.release()
            cv2.destroyAllWindows()
            return False

        for key in self.key_controls.keys():
            if chr(self.pressed) == key:
                self.key_controls[key]()
        return True

    def main_loop(self):

        _, frame = self.cam.read()
        self.h, self.w, _c = frame.shape

        # set current image frame to the processor's input
        self.processor.frame_in = frame
        # process the image frame to perform all needed analysis5
        self.processor.run(self.cam)
        # collect the output frame for display
        output_frame = self.processor.frame_out

        # show the processed/annotated output frame
        imshow("Processed", output_frame)

        # create and/or update the raw data display if needed
        if self.bpm_plot:
            self.make_bpm_plot()

        # handle any key presses
        return self.key_handler()