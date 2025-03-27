from django.shortcuts import render

class videoObect(object):
    channel = None
    link = None
    name = None
    description = None

class articlesObect(object):
    link = None
    name = None
    description = None

class imageObect(object):
    link = None
    name = None


def index(request): 
    videoArray = []
    articleArray = []
    imageArray = []
    video1 = videoObect()
    video1.channel = "The Ramsay Show Highlights"
    video1.link = "https://www.youtube.com/watch?v=-R1CLOuouYc"
    video1.name = "You're Burning A Lot Of Brain Calories To Only Make $1,000"
    video1.description = "Video from David Ramsay about saving 1000 dollars"
    videoArray.append(video1)
    video2 = videoObect()
    video2.channel = "The Ramsey Show Highlights"
    video2.link = "https://www.youtube.com/watch?v=lGHGzU3CtZg&list=PLN4yoAI6teRP0NWy4QLUWaylcBCJ5SnU-"
    video2.name = "The 7 Baby Steps Explained (Top Criticisms Addressed)"
    video2.description = "Video from David Ramsey about 7 baby steps"
    videoArray.append(video2)

    video3 = videoObect()
    video3.channel = "The Ramsey Show Highlights"
    video3.link = "https://www.youtube.com/watch?v=N8dpEzZ2Y_s"
    video3.name = "I won $3M and dont know what to do with it"
    video3.description = "Video from David Ramsey about what to do with 3 million dollars"
    videoArray.append(video3)
      
    video4 = videoObect()
    video4.channel = "The Ramsey Show Highlights"
    video4.link = "https://www.youtube.com/watch?v=VFx2iyTN2so"
    video4.name = "Im 21 and being pressured to finance a car"
    video4.description = "Video talking about financing a car at 21"
    videoArray.append(video4)

    video5 = videoObect()
    video5.channel = "The Ramsey Show Highlights"
    video5.link = "https://www.youtube.com/watch?v=tOAxxcLNk6I"
    video5.name = "This is how you recover from bankruptcy"
    video5.description = "Video talking about how to recover if you go bankrupt"
    videoArray.append(video5)

    video6 = videoObect()
    video6.channel = "Brenna Living Joyfully"
    video6.link = "https://www.youtube.com/watch?v=q5LsuqGcApU"
    video6.name = "Budgeting for beginners - how to make a budget from scratch 2025"
    video6.description = "Video talking about how to begin to make a budget"
    videoArray.append(video6)

    video7 = videoObect()
    video7.channel = "Shay Budgets"
    video7.link = "https://www.youtube.com/watch?v=3pslPbfpnzk"
    video7.name = "How to: the easiest and simplest way to create a monthly budget! 6-minute process"
    video7.description = "Video talking about how to set up a monthly budget"
    videoArray.append(video7)

    video8 = videoObect()
    video8.channel = "Elena Taber"
    video8.link = "https://www.youtube.com/watch?v=Pau88PAPD7Q"
    video8.name = "How to make a budget | Budgeting for beginners"
    video8.description = "Video talking about how to set up a budget"
    videoArray.append(video8)

    video9 = videoObect()
    video9.channel = "The Ramsey Show Highlights"
    video9.link = "https://www.youtube.com/watch?v=4Eh8QLcB1UQ"
    video9.name = "How do i make a budget and stick to it?"
    video9.description = "Video talking about how to set up a budget and stick to it"
    videoArray.append(video9)

    video10 = videoObect()
    video10.channel = "Work smarter not harder"
    video10.link = "https://www.youtube.com/watch?v=UAM1Ia5ZIp8"
    video10.name = "Excel Budget Teplate | Autommate your budget in 15 minutes"
    video10.description = "Video talking about how to set up a budget excel template"
    videoArray.append(video10)

    image1 = imageObect()
    image1.link = "https://www.ccu.com/wp-content/uploads/PROD-5338_Graphic-1-2880x1279.png"
    image1.name = "tips"
    imageArray.append(image1)

    image2 = imageObect()
    image2.link = "https://www.goodfinancialcents.com/wp-content/uploads/2023/09/15-Surprisingly-Simple-Money-Saving-Tips-for-Families-1024x713.png.webp"
    image2.name = "tips2"
    imageArray.append(image2)

    image3 = imageObect()
    image3.link = "https://cdn.prod.website-files.com/5f3f94d9ae99fbb1ea28cc2c/672dc780fae5f0083101e4f4_60054105eaf5d7da6bc52f22_Copy%2520of%2520Copy%2520of%2520Outbound%2520Creatives%2520(New)%2520(24).png"
    image3.name = "tips3"
    imageArray.append(image3)

    image4 = imageObect()
    image4.link = "https://cdn.educba.com/academy/wp-content/uploads/2024/12/Practical-Ways-for-Saving-Money-on-Everyday-Expenses.jpg"
    image4.name = "tips4"
    imageArray.append(image4)

    article1 = articlesObect()
    article1.name = "Voya"
    article1.link = "https://www.voya.com/page/financial-wellness-library?gad_source=1&gclid=Cj0KCQjwhYS_BhD2ARIsAJTMMQY6guUHIIQjSVMobZVvvBpZEPkfJSQimXIuyMbQnul7HehXqx-8EcUaApdpEALw_wcB&gclsrc=aw.ds"
    article1.description = "Good Source for tips fo investing saving money and other resouces"
    articleArray.append(article1)

    article2 = articlesObect()
    article2.name = "New York Life"
    article2.link = "https://www.newyorklife.com/articles/create-financial-strategy?tid=1371&cmpid=kncnb_AP_23MF_google_na_na_na_ctx_MAT_CFSM_na_0_0_0&gad_source=1&gclid=Cj0KCQjwhYS_BhD2ARIsAJTMMQYGIp_QdegtG0vnatsFUONOg4TQXZV8zbbPQSViiZj-4pXWHfN82_saAo82EALw_wcB&gclsrc=aw.ds"
    article2.description = "Good Source for making a financial strategy"
    articleArray.append(article2)

    article3 = articlesObect()
    article3.name = "Bank Of America"
    article3.link = "https://promotions.bankofamerica.com/consumer/financialwellness/managingspending?cm_mmc=EBZ-Retention-_-Google-PS-_-money_savings_advice-_-NB_Spending&gad_source=1&gclid=Cj0KCQjwhYS_BhD2ARIsAJTMMQZG1TQTlgsA4lXw8Wge7zHUBNz5QRnTbpXLzr2lme6MQ_anqrgDRC8aAiM5EALw_wcB&gclsrc=aw.ds"
    article3.description = "Good Source for financial help"
    articleArray.append(article3)

    article4 = articlesObect()
    article4.name = "Nerd Wallet"
    article4.link = "https://www.nerdwallet.com/article/finance/how-to-save-money"
    article4.description = "Good Source for finding ways to save money"
    articleArray.append(article4)

    article5 = articlesObect()
    article5.name = "Better Money Habits"
    article5.link = "https://bettermoneyhabits.bankofamerica.com/en/saving-budgeting/ways-to-save-money"
    article5.description = "Good Source for finding ways to save money"
    articleArray.append(article5)

    article6 = articlesObect()
    article6.name = "First First Financial Bank"
    article6.link = "https://www.bankatfirst.com/personal/discover/flourish/seven-money-saving-tips-you-might-overlook.html"
    article6.description = "Good Source for finding tips to save money"
    articleArray.append(article6)

    article7 = articlesObect()
    article7.name = "Intuit"
    article7.link = "https://www.intuit.com/solutions/education/?cid=ppc_G_p_US_.I4E_US_GGL_NonBrand_Search._basic%20financial%20literacy_txt&gad_source=1&gclid=Cj0KCQjwhYS_BhD2ARIsAJTMMQYPMyCDhCQgwdpK47tRZVnQ6wHyMh_AYxfMosRQa5vNn4EjtLG1vGgaAvLoEALw_wcB&gclsrc=aw.ds"
    article7.description = "Good Source for finding tips to save money"
    articleArray.append(article7)

    article8 = articlesObect()
    article8.name = "Investor.gov"
    article8.link = "https://www.investor.gov/additional-resources/spotlight/never-stop-learning?utm_source=google&utm_medium=cpc&utm_adgroup={AdGroupName}&utm_campaign={CampaignName}&gad_source=1&gclid=Cj0KCQjwhYS_BhD2ARIsAJTMMQY_fToKUMIifpmjOlUSrhhOuPrHcFmrU_-eFW-UHfnCRK-W5KhN1cYaAgzPEALw_wcB"
    article8.description = "Good Source for finding tips to save money"
    articleArray.append(article8)


    return render(request, "resources/recource.html", {'articleArray': articleArray, 'imageArray': imageArray, 'videoArray': videoArray})
def videos(request): 

    return render(request, "resources/videos.html")

def images(request): 

    return render(request, "resources/images.html")
def articles(request): 

    return render(request, "resources/articles.html")