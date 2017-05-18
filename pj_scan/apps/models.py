#_*_ coding:utf-8 _*_

from django.db import models  


DATA_TYPES = (
     (0, u'否'),
     (1, u'是'),
)


class BaseMsg(models.Model):  
    id = models.AutoField(primary_key=True)
    project = models.CharField(u"项目名称", max_length=255, blank=True, null=True)  
    department = models.CharField(u"业务部门", max_length=255, blank=True, null=True)  
    dns = models.CharField(u"域名", max_length=255, blank=True, null=True)  
    ip = models.CharField(u"内网ip地址", max_length=255, blank=True, null=True)  
    owner = models.CharField(u"负责人", max_length=255, blank=True, null=True)  
    tel = models.CharField(u"负责人电话", max_length=255, blank=True, null=True)  
    email = models.EmailField(u"负责人邮箱", blank=True, null=True)  
    devlang = models.CharField(u"开发语言或框架", max_length=255, blank=True, null=True, default="")  
    langver = models.CharField(u"开发语言版本", max_length=255, blank=True, null=True, default="")  
    webtype = models.CharField(u"Web类型", max_length=255, blank=True, null=True, default="")  
    webversion = models.CharField(u"Web版本", max_length=255, blank=True, null=True, default="")  
    osinfo = models.CharField(u"操作系统", max_length=255, blank=True, null=True, default="")  
    osversion = models.CharField(u"操作系统版本", max_length=255, blank=True, null=True, default="")  
    dbtype = models.CharField(u"数据库类型", max_length=255, blank=True, null=True, default="")  
    dbversion = models.CharField(u"数据库版本", max_length=255, blank=True, null=True, default="")  
    s_count = models.CharField(u"服务组件数量", max_length=255, blank=True, null=True)
    data_type = models.IntegerField(u"是否可扫描", choices=DATA_TYPES, default=1)
      
    def __unicode__(self):
        return self.id

    class Meta:
        db_table = "basemsg"    
        verbose_name = u"信息库"
        verbose_name_plural = verbose_name      


class SrvMsg(models.Model):  
    dip =  models.ForeignKey(BaseMsg, related_name="data_set", blank=True, null=True)
    midport = models.CharField(u"服务端口", max_length=255, blank=True, null=True)  
    midtype = models.CharField(u"服务名", max_length=255, blank=True, null=True)  
    midversion = models.CharField(u"服务版本", max_length=255, blank=True, null=True)  
      
    #def __unicode__(self):  
    #    return "%s-%s-%s"% (self.midport, self.midtype, self.midversion)
    def __unicode__(self):  
        return "{'port':'%s', 'name':'%s', 'version':'%s'}"% (self.midport, self.midtype, self.midversion)
   # def __dict__(self):  
    #    return {"port":self.midport, "name":self.midtype, "version":self.midversion}
      
    class Meta:  
        db_table = "srvmsg"    
        verbose_name = u"组件详情"
        verbose_name_plural = verbose_name 



class ApiMsg(models.Model):  
    id = models.AutoField(primary_key=True)
    ip = models.CharField(u"IP", max_length=255, blank=True, null=True)  
    port = models.IntegerField(u"port", blank=True, null=True, default=80)  
    code = models.CharField(u"返回码", max_length=255, blank=True, null=True)  
    msg = models.CharField(u"详情", max_length=255, blank=True, null=True, default='ok')  
      
    def __unicode__(self):  
        return self.id
      
    class Meta:  
        db_table = "apimsg"    
        verbose_name = u"API详情"
        verbose_name_plural = verbose_name 
