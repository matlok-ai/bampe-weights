import logging
import bw.bl.run_ai_training_visualizer as run_viz


logging.basicConfig(
    # lots of debugging
    # level=logging.DEBUG,
    level=logging.INFO,
    format=(
        "%(asctime)s.%(msecs)03d %(levelname)s "
        "%(funcName)s - %(message)s"
    ),
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


if __name__ == "__main__":
    # start the v1 training visualizer
    run_viz.run_ai_training_visualizer()
