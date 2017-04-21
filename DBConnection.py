# coding=utf-8
import pymssql

class DBConnect:
        try:
            con = pymssql.connect(server='WINJIT214', user='sa', password='winjit@123', database='ServerSocket')
            c = con.cursor()
            def Login_Insert(self,equipment,port,ip_address,numData):
                    query = self.c.callproc('sp_LoginDetails', (port, ip_address, equipment,numData))
                    self.con.commit()

            def SamplingData(self,equipment,port,ip_address,temperature,RH,HotWater,ColdWater,Defrosting,TDS,ActualV):
                    query = self.c.callproc('sp_SamplingData', (port, ip_address, equipment, temperature,RH,HotWater,ColdWater,Defrosting,TDS,ActualV))
                    self.con.commit()

            def PowerWater(self,equipment,port,ip_address,power,water,ActualVal):
                    query=self.c.callproc('sp_PowerWater',(port,ip_address,equipment,power,water,ActualVal))
                    self.con.commit()

            def TimeDuration(self,equipment,port,ip_address,obtain):
                    query = self.c.callproc('sp_TimeDuration', (port, ip_address, equipment, obtain))
                    self.con.commit()

            def FilteringTime(self,equipment,port,ip_address,Filter1,Filter2,Filter3,Filter4,Filter5,Filter6,Filter7,ActualValue):
                    query = self.c.callproc('sp_TimeFiltering', (port, ip_address, equipment,Filter1,Filter2,Filter3,Filter4,Filter5,Filter6,Filter7,ActualValue))
                    self.con.commit()

            def ErrorMessage(self, equipment, port, ip_address,unit,errorCode,msg):
                query = self.c.callproc('sp_ErrorMessage', (port, ip_address, equipment, unit,errorCode,msg))
                self.con.commit()

        except Exception, e:
            str(e)

        finally:
            con.close