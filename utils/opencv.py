"""Utility for making convenient use of OpenCV."""

from typing import Any, List, Optional, Tuple, Union

import cv2
import numpy as np

from video_processing_engine.vars.color import green, yellow


def rescale(frame: np.ndarray,
            width: Optional[int] = 300,
            height: Optional[int] = None,
            interpolation: Optional[Any] = cv2.INTER_AREA) -> np.ndarray:
  """Rescale the frame.
  
  Rescale the stream to a desirable size. This is required before
  performing the necessary operations.

  Args:
    frame: Numpy array of the image frame.
    width: Width (default: None) to be rescaled to.
    height: Height (default: None) to be rescaled to.
    interpolation: Interpolation algorithm (default: INTER_AREA) to be
                   used.

  Returns:
    Rescaled numpy array for the input frame.

  Example:
    >>> import cv2
    >>> from video_processing_engine.utils.opencv import rescale
    >>> 
    >>> stream = cv2.VideoCapture(0) 
    >>> 
    >>> while True:
    ...   _, frame = stream.read()
    ...   frame = rescale(frame, width=300, interpolation=cv2.INTER_LANCZOS4)
    ...   cv2.imshow('Test feed', frame)
    ...   if cv2.waitKey(5) & 0xFF == int(27):
    ...     break
    >>> stream.release()
    >>> cv2.destroyAllWindows()
    >>>
  """
  dimensions = None
  frame_height, frame_width = frame.shape[:2]
  # If both width & height are None, then return original frame size.
  # No rescaling will be done in that case.
  if width is None and height is None:
    return frame
  if width and height:
    dimensions = (width, height)
  elif width is None:
    ratio = height / float(frame_height)
    dimensions = (int(frame_width * ratio), height)
  else:
    ratio = width / float(frame_width)
    dimensions = (width, int(frame_height * ratio))
  return cv2.resize(frame, dimensions, interpolation=interpolation)


def disconnect(stream: np.ndarray) -> None:
  """Disconnect stream and exit the program."""
  stream.release()
  cv2.destroyAllWindows()


def draw_box_with_tuple(frame: np.ndarray,
                        start_xy: Tuple,
                        end_xy: Tuple,
                        color: Optional[List] = yellow,
                        thickness: Optional[int] = 1) -> None:
  """Draw bounding box around the detected faces.

  Bounding box adjusts automatically as per the size of faces in view.

  Args:
    frame: Numpy array of the image frame.
    start_xy: Tuple of top left coordinates.
    end_xy: Tuple of bottom right coordinates.
    color: Bounding box color (default: yellow)
    thickness: Thickness (default: 1) of the bounding box.

  Note:
    This method is only applicable to the faces detected by CaffeModel.
    For faces detected by Haar cascade, use 'detect_motion()'.
  """
  return cv2.rectangle(frame, start_xy, end_xy, color, thickness)


def detect_motion(frame: np.ndarray,
                  x: Union[int],
                  y: Union[int],
                  w: Union[int],
                  h: Union[int],
                  color: Optional[List] = green,
                  thickness: Optional[int] = 1) -> None:
  """Draw bounding box around the detected objects.

  Bounding box adjusts automatically as per the size of object(s) in the
  view.

  Args:
    frame: Numpy array of the image frame.
    x: Top left X-position of the detected object.
    y: Top left Y-position of the detected object.
    w: Bottom right X-position of the detected object.
    w: Bottom right Y-position of the detected object.
    color: Bounding box color (default: green)
    thickness: Thickness (default: 1) of the bounding box.
  """
  return cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness)
