# 끄적끄적
![HTML](https://img.shields.io/badge/html-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![css](https://img.shields.io/badge/css-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)
![Apache Hadoop](https://img.shields.io/badge/Apache%20Hadoop-66CCFF?style=for-the-badge&logo=apachehadoop&logoColor=black)
![Apache Spark](https://img.shields.io/badge/Apache%20Spark-FDEE21?style=flat-square&logo=apachespark&logoColor=black)
![MySQL](https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
-
<img width="1242" alt="image" src="https://github.com/MalLang27dsde/MalLang/assets/135773366/e4574216-2187-4170-97d3-fbfdb62e812a">
<h3>주제 선정</h3> 
일상은 각기 다른 이야기와 감정으로 가득 차 있다. 그 이야기나 감정을 말로만 표현하기에 때로 부족함을 느끼곤 한다. 우리는 그림으로 그 이야기를 표현해보고자 한다. "내가 쓰면 대신 그려주는
그림일기 끄적끄적"은 이런 아이디어에서 시작되었다.
사용자가 일기를 작성하면, 우리는 그 일기의 내용을 바탕으로 관련된 그림을 자동으로 생성해준다. 이 그림은 단순한 꾸밈 요소가 아닌, 사용자의 감정과 생각을 시각적으로 표현하는 미디어로서의
역할을 한다. 텍스트만으로는 전달되지 않는 미묘한 뉘앙스나 감정의 농도, 그리고 그날의 기분을 그림을 통해더욱 생생하게 기록할 수 있다. 우리의 그림일기 프로젝트를 통해 일기를 쓰는 사용자에게 소중한
추억을 멋진 그림과 함께 저장하고, 나중에 그날의 기분과 생각을 다시 떠올릴 수 있게 도와주려고 한다.
<h3>기획 배경</h3>
본인의 감정을 인식하지 못하거나 표현하지 못해서 정신 질환을 겪는 사람들이 많다. 감정을 시각화하고 표현하여 문제를 해소할 수 있는 방안이 필요하다.
    그림일기에서 글과 그림은 상호보완적으로 자기이해를 증폭시키는 역할을 한다. 그림일기를 창작하는 것뿐만 아니라, 그림을 본다는 것만으로도 물리적 자극 이상의 것으로 정서를 환기한다.
<h3>분석 목표</h3>
<div>1) 한국어 요약 모델 개발 </div>
<div>2) 한국어-영어 번역 모델 개발</div>
<div>3) 크롤링을 통한 일기 데이터 수집 및 활용</div>
<div>4) 공공 OPEN API 데이터 활용</div>
<div>5) 데이터 파이프라인 구축</div>
<br>
<div>
  <div>말랑스 : <a href="https://github.com/yeonjin99">장연진</a>
                <a href="https://github.com/yadoran99">서혁준</a>
                <a href="https://github.com/hyony2">이효은</a>
                <a href="https://github.com/seokwon22">최석원</a>
                <a href="https://github.com/xaeyoungkim">김태영</a>
  </div>
</div>
<h3>모델</h3>
<div>끄적끄적은 한국어형 그림일기 생성 서비스 입니다. </div>
<h5>1. 한국어 요약모델 : PageRank & TextRank</h5>

<h5>2. 한국어 번역 모델 : Seq2Seq & Attention </h5>


<div>

      mallang

      └ mallang_model
      
            └ Mallang
      
       └ summary.pt
 
       └ translate
 
             └ transformer
       
             └ save
       
                  └ pt파일 추가
</div>
<h4>한국어 번역 모델 pt파일</h4>
https://drive.google.com/file/d/1OBh2Hk1X3vYVW4IfPHxc6ysN28wUXDIR/view?usp=drive_link

<h3>API</h3>

<a href="https://platform.openai.com/account/api-keys"><h5>1. DALL·E 2</h5></a>
<a href="https://api.ncloud-docs.com/docs/ai-naver-clovavoice-ttspremium"><h5>2. TTS</h5></a>

<h3>pipeline</h3>
<img width="850" alt="image" src="https://github.com/MalLang27dsde/MalLang/assets/135773366/a41fb8f2-ebe7-4270-b620-a4131ea6caff">
<h3>version</h3>

* ubuntu 18.02 version
* java 11 version
* python 3.9.18 version
* hadoop 3.3.6 version
* zeppelin 0.10.1 version
* spark 3.2 version
* mysql 8 version
* diango 4.2 version


<h3>서비스시현</h3>
https://drive.google.com/file/d/1G58TfTKgdzPj1DAigf5Es-kb299Kmjw1/view?usp=drive_link


