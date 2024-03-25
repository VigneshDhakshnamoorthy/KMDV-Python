import configparser
import os
import json
from datetime import datetime
import win32com.client

class MailConfig:

    iniFilePath: str = "resource/config/mailConfig.ini"
    config = configparser.ConfigParser()
    config.read(iniFilePath)
    @staticmethod
    def getSignatureEmail() -> str:
        return MailConfig.config.get("Report", "SignatureEmail")
    
    @staticmethod
    def isReportMail() -> bool:
        return MailConfig.config.getboolean("Report", "ReportMail")

    @staticmethod
    def getEmailList() -> list[str]:
        emailList: list[str] = MailConfig.config.get("Report", "ToEmail").split(",")
        return [emailid for emailid in emailList]

    @staticmethod
    def send_test_report(dateTime: str, pass_count:int, fail_count:int, skip_count:int):
        subject:str = f"Test Automation Report"
        body:str = f"""<html><body><div><div><b>Hi Team,</b><br><br>
                        The Smoke Test Execution Using Selenium with python in Production Environment started at 
                        <span style="color:#993300"><em>{dateTime}</em></span>. <br>
                        Please open attachment for more details. Below are the results, 
                        <br><br>
                        <table style="width:60%">
                        <tr>
                        <td><b><span style="color:#008000">Passed</span><br aria-hidden="true"></b></td>
                        <td><b><span style="color:#ff0000">Failed</span></b><br aria-hidden="true"></b></td>
                        <td><b><span style="color:#FFA500">Skipped</span></b><br aria-hidden="true"></b></td>
                        <td><b><span style="color:#254DEE">Total</span><br aria-hidden="true"></b></td>
                        </tr>
                        <tr>
                        <td><span style="color:#008000">{pass_count}</span><br aria-hidden="true"></td>
                        <td><span style="color:#ff0000">{fail_count}</span></b><br aria-hidden="true"></td>
                         <td><span style="color:#FFA500">{skip_count}</span></b><br aria-hidden="true"></td>
                        <td><span style="color:#254DEE">{pass_count + fail_count+ skip_count}</span><br aria-hidden="true"></td>
                        </tr>
                        </table>
                        <br>We are always happy to accommodate our clients with assistance <br>if necessary! Please contact the below QA Team <br>
                        <a href="mailto:{MailConfig.getSignatureEmail()}" >{MailConfig.getSignatureEmail()}</a> 
                        <br><br aria-hidden="true"><b>Thanks & Regards, </b><br>QA Team</div></div></body></html>"""
        try:
            
            outlook = win32com.client.Dispatch("Outlook.Application")
            mail = outlook.CreateItem(0)
            mail.Subject = subject
            mail.HTMLBody = body
            for emilid in MailConfig.getEmailList():                
                mail.Recipients.Add(emilid)                
            mail.Recipients.ResolveAll()
            mail.Send()
            print("Email sent successfully!")

        except Exception as e:
            print("Failed to send email:", str(e))

