# -*- coding: utf-8 -*-

"""

Created on Wed May 23 12:45:17 2018

@author: Nimit

"""
from flask import Flask,Response,render_template,send_from_directory
from flask import request
from flask_cors import CORS
from werkzeug.utils import secure_filename
import re
from difflib import SequenceMatcher
import json
import os
from PyPDF2 import PdfFileReader
#import psycopg2

path = os.getcwd()
print(path)
port = int(os.getenv("PORT", 3000))
upload_folder = path
ALLOWED_EXTENSIONS = set(['pdf','docx'])
app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = upload_folder

skill_dictionary = ['fico','jquery','jpawithhibernate','servlets','knockoutjs','cygwin','cobol','greenhattool','microservices','micro-services','microservices','apigee','reddis','d3js','casper','c#','jdbc','calendar','linq-to-sqlclasses','serialportcommunicationprotocol','dataadapter','imsdb','uipath','coe','cpo','grailsframework','jstl','restful','docave','supportcentralframeworks','arisbpm','fxcop','gitlab','ef','jenkins','oracle','digiforms','clientinteraction','networking&monitoring','cucumber','golang','websphere','oraclefinancialsebusiness12','problemmanagement','jndi','sda','entityframework','computernetworks','css','soxcompliance','cloud','contractandcasemanagement','cgi-perl','coldfusion','polymer','jee5','payroll','em7database','gitbash','matlab','performancetuning','cloudfoundryoracle','automation','prince2','bigdatadevelopment','ejb','log4j','rpa','oktaadministration','algorithms','soap','supplychainmanagement','stormware','nodejs','legacyinteractions','identity&accessmanagement','tfs','full','microservice','security','cognos','xml','bi-dwh','grcanditsecurity','mainframedatabasedb2(z/os)','office365','tableau','wpf','cassandra','fedora21','distributed','polymerjs','teambuilding','teamhandlingtechnicalsupport','jsp','jax-ws','csv','obia','almintegration','dojo','est','stetonc++','soapui','spring','mulesoft','hoovers','seu','cvent','linux','pig','shellscripting','query/400','ide','telecomsector','jcl/sort','aprimo','tandem','backbonejs','dos','oracle11g','ms-office','angularjs','mainframesc','springmvc','implementer','dataset','dataadmintoolkit','datascience','sharepointsupport','rulelanguage','qlikview','uat','teamleadership','windows10','appservers','jax','stack','sqlite','caworkloadautomation','hoovers.net','linq2c#','backbone.js','newscale','python2.5','programmanagement','underscorejs','java/linux','service','ca7scheduler','maven','embeddedcandmicroprocessor8051','webapi','sass','powerbuilder','deployment','filenet','windows8.1','itslacatalogue','springmvc','mongodb','angular','datascience','esf','relational','predix14.2','corejava','jboss','hudson','projectlead','servicetesting','boot','clle','batchscripting','sasprogramming','karmajasmine','perl','sccm','jee','pl/sql','android','mapreduce','microsoftsqlserverintegrationservices(ssis)','json','macrobatch','exceptionhandling','idms','servicenow','jsf','foundation','mvcarch','replacements&depotrepair','uwp(universalwindowsplatform)','designpatterns','oraclebusinessintelligencepublisher','deep','workforceintegrationmanager','angularjs','impala','itsupport','jbuilder','tomcatas','itil','exacttarget','ibmas/400','payment','unittesting','aws','edivb','programmingandadministration','experienced','googlegolang','azure','iot','test','microprocessor8051','repairoutsourcing','photoshop','tortoisesvn','dt','.netframework','patterns','kendoui','bankingsoftwaretechnology','vuejs','angular2','client/server','ajax','buginvestigationandfixing','microsoftproject','clearcase','wordpress(admin','dataquality','sybase','k2','design','code','backbone','returns','businessmanagement','quest','solutiondevelopment','understandingofbusinessandprocesses','digital','"','automationanywhere','as','itrisk&securityhtml','cloudfoundry','asp.ne','sentry','implementation','visual','bmcremedy','escalationhandling','thread','silverlight','msvisualsourcesafe','springorm','pt','insidesales','microsoft','object','technicalsupport','javarmi','biz-talk','ile','broadvision','infragistics','ciscoserviceportal','problemsolving','jpa','release','corejava','eclipselink','rad','responsivewebdesign','changeman','hld','quicktestpro','sso','maximotechnical','sonarqube','centralized','rolebasedaccesscontrol','agile','ascendant(ibmtool)','deployementtools','webserver','jcl','mis','hotdocsjava','pdm','automationanywhere','absencemanagement','appworx','html5','functionaltesting','interpersonal','monitoring&controllingprojects','sapmm','lead','osgi','level3applicationsupport','finance','databasetesting','phonegap','retailpos','ordertocash(f&a)','sap-edi','ai','predix2','mssql','springboot','budgetinganddebt','releasemanagement','webscrapping','development','accruals','np6restaurantsupportcorejava','spring4','rally','ssis','mongodb','spring3.0','seleniumautomation','vpn&usersoftwaretroubleshooting','"akana','accountpresales','newrelic','bankingsector','dundasdashboard','control','andlebarjs','swing','msproject','customerconnect','aptospos','technicaldesign','jira','etcs','requirementsgathering','bootstrapjs','sqlrpgle','machinelearning','javamail','requirejs','xml1.1','windowsforms','sapbasis','visio(ms)','leadership&managementskills','mainframedeveloper','appdynamics','puppet','powerbuilder5.0','sox','gms','ibmiseriesi5-i7systemadministration','editpad','nosql','angular4','rotational','buildandreleasemanagement','smo','oracleetpm/ouaf','redhatlinux','scrummaster','oracle12c','primefaces','servlet','xsd','weblogic','windows7','hadoopclusterconfiguration','hibernate','oracle9i','galaxyas400','microservices','citrixxenapp','java/j2ee','ssrs','pl','ssrsreports','r','.net','businessanalyst','multithreading','activedirectory','reactjs','webapplicationdevelopment','vb6.0','elasticsearch','mvc6','ipadappdevelopment','windowscommnfoundation','jmeter','servlet-jsp','plsql','ws','telerik','analysis','hadoop','risk','os400','micro','linq-to-sqlclasses','blueprism','iis','photo-genic/graph','framework','ba','modal','oracletoplink','cordova','sapbobj','ldap','businessnegotiation','sas-di','services','javascript','trackwise','packager','batch','infopath','ms-access','server','extjs','git','j2eesolutionarchitect','microsoft.net','scripting','version','openjpa','team','junit','testdirector','sketching','underscorejs','ant','ibmiseries','itsecurityriskassessment','incident','aftersalesservice','vbscript','h-base','eaglepace','tableaufusioncharts','tal','oracledbaoverview','uml','jasperreport','us&non-uspayroll','web','intellij','edi','applicationsupport.ne','tibcoportal','ado.net','appserver','servicedesktroubleshooting','salesforce(admin)','vss','decisionmaking','konyide','productsupport','vmwarecloud','webspheremessagebroker','c++','oraclesql','akana','rabbitmq','dpro','ml','flume','lifesciencessector','businessverification','visualstudio2010','grc','richfaces','python','windows8','univision','winscp','obieereports','oracleebs','rsa','hpsm','oil','liferay','sql','contentmanagement','nintex','springtoolsuite','liferayportal','ibatis','wsdl','adobeflex','linq','vbscript','soa','stbt','technicalevaluation','angular2','developer','angular4','installshield','telecom','ibmmq','dev-ops','reviewboard','itinternalaudit','tsql','datastructures','ionic','unixadmin','linuxsolaris','microsoftvss','sfdc','merging','php','ireporttool','mocha','mainframe–jcl','rdlcreports','informatica-bi','sharepointonline','surfingiotupdates','node','assemblerprogramming','projmgmt','crm','dataanalytics','cicsandoops','dhtml','websphere','s3','servicecaféticketingtool','qtcreatordatabase','orm','alosadd','sapabap','webdesigning','apimanagement','windowsxp/nt','java','xhtml','oracle7.3','rubyonrails','wsad','vsamc','csd','jp','obiee','informatica','lambda','netbeanside','mvs','2013tfs','microsoftazure','nginx','regulatorycompliance','frameworkjava','talend','qa','wsdl/xsd','cloudera','merlin','studio','sourcetree','rds','problemchange','infrastructuresupport','excel','ciscoprimeservicecatalog','angular6','hive','citrix','html','agri-chemicalssector','leanexpert','mvc','oracleanalytics','mainframes','entityframework','predix','salesforce(sfdc)','sapdashboards','itilservicemanagement','servicedeskanalyst','ilm','unix','muleesb','productionsupport','unixshellscripting','tidalenterpriseorchestrator','visualc','ems','n2k','monitoringtechnologies','msaccess','mining','winforms','webflow','datavalidation','teradata','sentry"','delphi7.0','office365administration','cl','springboot','webservices','jms','rpgile','ftp','artificialintelligence','changemanagement','j2ee','docker','foundationframework','solution','msbi','advancedjava','healthcaresector','manual','springsecurity','ms','postgres','sqlserver','bootstrap','driven','controltesting','oracleapplicationserver9i','elasticsearch','blaze7.2','testing','coderefactoring','applicationtransitionmanagement','iq','ansiable','mysql','devtools','badi','teamleader','itil','c','servlet2.2','middleware','vb','.netwithmvc','crystalreport','customerconnec','gxs','fpestimation','websphereadmin','deeplearning','tomcat','sammuyjs','kawa','ccna','microsoftdynamicsax','cicsc','googledocsautomation','resharper','mvc4','dbfit','underscore','struts','clicksoftware','functionalconsultant','rest','executivemanagement','intelpentium','asp.net','beaweblogicportal9.2','idoc','manualtesting','middlewarejcaps','angular5','sun-solaris2.7','db2','qtp','hploadrunner','architect','legacy','powerpoint','dac','sap(fico)','svn','pm','owasp','professionalservices','powershell','splunk','vlookup','cvs','mybatis','spock','j2se','java3.5','aop','cycle','peoplemanagement','retailbasedtroubleshooting','servicedeskmanagement','selenium','testcases', 'defecttracking', 'regressiontesting', 'appserverdeployment', 'relationaldatabases', 'communicationskills', 'css3', 'ionicframework', 'ooad', 'objectorienteddesignpatterns', 'testdrivendevelopment', 'datastructureandalgorithms', 'interpersonalskills', 'projectmanagementskills', 'stakeholdermanagement', 'resourcemanagement', 'riskassessment', 'remediation', 'requirementsgatheringanalysis', 'cloudandmicroservicesarchitecture', 'springbatch', 'angularjs1.4', 'angularjs1.5', 'jbossas', 'esfframework', 'digitalthread', 'codesetup', 'microsoftvisualstudio2016', 'teamfoundationserver-tfs', 'mscrmsolutionpackager', 'managecentralizeddata', 'verbalcommunication', 'writtencommunication', 'distributedagile', 'peoplemanager', 'devops', 'intellijide', 'telecomindustryexperience', 'peercodereview', 'rediscache', 'redis', 'apachetomcat', 'behavioraltesting', 'timemanagementskills', 'uxdesign', 'protopagesdesigning', 'liquiddesign', 'ui', 'windows', 'wildfly', 'sqlservermanagementstudio', 'axis2framework', 'xm', 'xslt', 'incidentmanagement', 'batchjobserver', 'troubleshootingskills', 'illustrator', 'nunit', 'jasmine', 'less', 'grunt', 'gulp', 'bower', 'npm', 'webpack', 'mvvm', 'analyticalskills', 'chef', 'ci', 'cd', 'automationtesting', 'windowsscripting', 'extensiblemarkuplanguage(xml)', 'sap', 'asp', 'atlassianjira', 'swift', 'phython', 'pascal', 'erlang', 'clojure', 'labview', 'vb.net', 'lisp', 'algol', 'swift', 'objectivec', 'angular1', 'go', 'lua', 'rust', 'haskell', 'arduino', 'shell', 'scala', 'ios', 'vba', 'lux', 'lamda']

@app.route('/uploader', methods = ['POST'])
def upload_file():
    try:
        f = request.files['file']
        f.save(secure_filename(f.filename))
        result = 'success'
        msg = {"upload": result}
        resp = Response(response=json.dumps(msg),
                        status=200,
                        mimetype="application/json")
        return resp
    except Exception as e:
        print(e)


@app.route('/extractPdf', methods = ['POST'])
def extractPdf():
    try:
        req_body = request.get_json(force=True)
        #s = req_body['string'].lower()
        # this gives list of words
        name = req_body['name']
        text = getPDFContent(name)
        wordList = g_solution(text)
        print("list of words",wordList)
        coun = req_body['count']
        #count = extract_count(wordList)
        # this gives me list of skills
        result_dup = iterate_list(wordList)
        result_set = set(result_dup)
        result = list(result_set)
        print("duplicate elements",result)
        print("result",result)
        msg = {"demand_skills":result,"count":coun}
        resp = Response(response=json.dumps(msg),
        status=200,
        mimetype="application/json")
        return resp
    except Exception as e:
        print(e)

@app.route('/extract', methods = ['POST'])
def extract():
    try:
        req_body = request.get_json(force=True)
        text = req_body['string'].lower()
        # this gives list of words
        wordList = g_solution(text)
        print("list of words",wordList)
        coun = req_body['count']
        #count = extract_count(wordList)
        # this gives me list of skills
        result_dup = iterate_list(wordList)
        result_set = set(result_dup)
        result = list(result_set)
        print("duplicate elements",result)
        print("result",result)
        msg = {"demand_skills":result,"count":coun}
        resp = Response(response=json.dumps(msg),
        status=200,
        mimetype="application/json")
        return resp
    except Exception as e:
        print(e)

'''
def fetch():
    try:
        sql = 

    except Exception as e:
        print(e)
'''

def getPDFContent(name):
    try:
        content = ""
        pdf = PdfFileReader(name, "rb")
        for i in range(0, pdf.getNumPages()):
            content += pdf.getPage(i).extractText() + "\n"
            content = " ".join(content.replace("\xa0", " ").strip().split())
        print("content\n",content)
        return content
    except Exception as e:
        print(e)

'''
def extract_count(wordList):
    try:
        count = 0
        print("fun_list",wordList)
        for iter in range(1,len(wordList)):
            if wordList[iter-1] is 'need' or 'vacancy':
                if wordList[iter] is re.match('(?:\b|-)([1-9]{1,2}[0]?|100)\b',wordList):
                    count = wordList[iter]
        print("count",count)
        return count
    except Exception as e:
        print(e)
'''
def g_solution(sample_text):
    try:
        wordList = re.sub("[^\w.]", " ", sample_text).split()
        #print(wordList)
        return wordList
    except Exception as e:
        print(e)

def iterate_list(wordList):
    try:
        #print("wordlist\n",wordList)
        req_skills=[]
        for j in range(0,len(wordList)):
            str_compare_1 = wordList[j]
            str_compare_2 = wordList[j-1] + wordList[j]
            str_compare_3 = wordList[j-2]+ wordList[j-1]+wordList[j]
            #print("Skill_dictionary\n",skill_dictionary)
            if (str_compare_3 in skill_dictionary):
                req_skills.append(str_compare_3)
            if (str_compare_2 in skill_dictionary):
                req_skills.append(str_compare_2)
            if (str_compare_1 in skill_dictionary):
                req_skills.append(str_compare_1)
        print(req_skills)
        result = bridge(req_skills)
        return result
    except Exception as e:
        print(e)

def bridge(list):
    try:
        dup_list = list[:]
        for i in range(0,len(list)):
            prob = similar(list[i-1],list[i])
            print(list[i-1],list[i],prob)
            if prob > 0.4:
                dup_list.remove(list[i-1])
        return dup_list
    except Exception as e:
        print(e)

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

if __name__ == '__main__':
    app.run(port=port)