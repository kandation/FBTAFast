```python
if self.__stopCounter >= self.db.clusters_num:
    log(':mManage:  END LOOP')
    self.__is_manager_running = True
```
มีปัญหาตรงที่ว่า หาก...ทดลองแปป