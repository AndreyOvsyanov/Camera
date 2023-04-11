import cv2

from typing import List
from helpers import get_name_folder, SHAPE

class VideoWriter:
    def __init__(self, videos: List[cv2.VideoCapture]):
        self.output, self.videos = [], []
        for iter, video in enumerate(videos):
            self.videos.append(video)
            self.output.append(
                cv2.VideoWriter(
                    'Records/{}out{}.avi'.format(get_name_folder(), iter+1),
                    cv2.VideoWriter_fourcc(*'XVID'),
                    60.0,
                    SHAPE
                )
            )


    def recording(self):
        while True:
            successes, frames = [], []
            for iter in range(len(self.videos)):
                success, frame = self.videos[iter].read()
                successes.append(success)
                frames.append(frame)

            if all(successes):
                for iter in range(len(self.output)):
                    self.output[iter].write(frames[iter])
                    cv2.imshow('{}'.format(iter + 1), frames[iter])

            if cv2.waitKey(1) == ord('q'):
                break

        for iter in range(len(self.videos)):
            self.output[iter].release()
            self.videos[iter].release()

        cv2.destroyAllWindows()

videos = [cv2.VideoCapture(iter) for iter in range(2)]
video = VideoWriter(videos=videos)
video.recording()