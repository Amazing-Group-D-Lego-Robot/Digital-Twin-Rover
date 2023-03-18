For the file you enter from    
``` python
import logging
log_level = logging.Debug

#Instantiate logger
logger = logging.getLogger(__name__)
logger.setLevel(log_level)

# define handler and formatter
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")    

# add formatter to handler
handler.setFormatter(formatter)

#add handler to logger
logger.addHandler(handler)
 
    
logging.basicConfig(level=log_level, format='%(asctime)s :: %(levelname)s :: %(message)s')
```
With the file your logging in outside of this doing the following:

```python
import logging

logger = logging.getLogger(__name__)
```

Then if you want to raise you can do so at different point
e.g.
```python
logger.info("message")
logger.debug("message")
logger.warning("message")
logger.error("message")
logger.critical("message")
```

