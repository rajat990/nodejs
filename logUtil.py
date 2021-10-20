import logging
import os
from datetime import datetime

logger = logging
file_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(file_dir, 'logs')
if not os.path.exists(log_path):
    os.makedirs(log_path)
log_file = os.path.join(log_path, 'chatbot-%s.log' % datetime.now().strftime("%Y%m%d-%H%M%S"))

logger.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO,
                    datefmt='%a, %d %b %Y %H:%M:%S', filename=log_file)

logger.getLogger(__name__)