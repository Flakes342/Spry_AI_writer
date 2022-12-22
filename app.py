from datetime import datetime
import streamlit as st
import pandas as pd
import uuid
import openai
import firebase_admin
from firebase_admin import credentials, firestore, storage


storage_config = {"storageBucket": "assessment-portal-70b0e.appspot.com"}
cred = credentials.Certificate("cfg.json")
firebase_admin.initialize_app(cred, storage_config)

db = firestore.client()
bucket = storage.bucket()


def save_query(result):
    idx = str(uuid.uuid4())
    doc_ref = db.collection("content-ai-gpt").document(idx)
    doc_ref.set({"parameters": result})
    return


def main_page():
    st.markdown("# AI CONTENT WRITER")
    st.write(
        "Here you can create blogs, write descriptions, captions and so much more using AI!"
    )
    

def blog():
    st.write(
        """
    # Blog writer
    This app can create a mini blog for any topic!
    """
    )

    def user_input_features():
        Prompt = "Write talking points for the topic " + st.text_input(
            "Enter blog title"
        )
        return Prompt

    Prompt = user_input_features()
    if st.button("Generate"):
        if Prompt != "Write talking points for the topic ":

            nums = []
            for i in range(100):
                nums.append(str(i))

            openai.api_key_path = ".env"
            # str1 = str(input("Please enter the name of the topic for the blog:"))
            # str2 = "Write talking points on the topic reducing neck and back pain at work"
            # prompt1 = str2 + str1

            def getpoints(Prompt):
                response = openai.Completion.create(
                    model="text-davinci-002",
                    prompt=Prompt + ":",
                    temperature=0.6,
                    max_tokens=469,
                    top_p=1,
                    frequency_penalty=1,
                    presence_penalty=1,
                )

                lis = []
                lis = response["choices"][0]["text"].split("\n")
                plist = []
                for i in range(len(lis)):
                    if lis[i] != " " and lis[i] != "":
                        plist.append(lis[i])

                for i in range(len(plist)):
                    if plist[i][0] == "-":
                        plist[i] = plist[i][1:]
                    if plist[i][0] in nums:
                        plist[i] = plist[i][2:]
                return plist

            # print (getpoints(prompt1))

            def expandPoints():
                plist = getpoints(Prompt)
                p2lis = []
                p3lis = []
                for i in plist:
                    response = openai.Completion.create(
                        model="text-davinci-002",
                        prompt=i,
                        temperature=0.6,
                        max_tokens=469,
                        top_p=1,
                        frequency_penalty=1,
                        presence_penalty=1,
                    )
                    p3lis.append(response["choices"][0]["text"])
                    p2lis.append(i + response["choices"][0]["text"])

                return (plist, p2lis, p3lis)

            # print (expandPoints())

            x = expandPoints()[1]
            y = expandPoints()[2]
            z = expandPoints()[0]
            res_str = ""
            for i in range(len(x)):
                res_str += str(x[i]) + " "

            def getKeywords(res_str):
                p3lis = []
                response = openai.Completion.create(
                    model="text-davinci-002",
                    prompt="Extract keywords from this text:" + "\n" + res_str,
                    temperature=0.3,
                    max_tokens=60,
                    top_p=1,
                    frequency_penalty=0.8,
                    presence_penalty=0,
                )
                p3lis.append(response["choices"][0]["text"])

                return p3lis

            key = getKeywords(res_str)[0]

            df = pd.DataFrame(
                {
                    "Title": Prompt.replace("Write talking points for the topic ", ""),
                    "Blog": res_str,
                    "timestamp": datetime.datetime.utcnow(),
                },
                index=[0],
            )

            result = {
                "Title": Prompt.replace("Write talking points for the topic ", ""),
                "Blog": res_str,
                "timestamp": datetime.datetime.utcnow(),
            }

            df.to_csv("spry_blog.csv", mode="a", index=False, header=False)
            save_query(result)

            if Prompt != "Write talking points for the topic":

                st.subheader(Prompt.replace("Write talking points for the topic ", ""))

                for i in range(len(x)):
                    st.write(z[i])
                    with st.expander("Expand"):
                        st.write(x[i])

                    st.write("--------------------------")

            else:
                st.write("Well, I am an AI but enter the name of the topic atleast")

            st.write(
                """
            ## Keywords:
            """
            )
            st.write(key)
            print("Done")


def description():
    st.write(
        """
    # Description writer
    This app can create a description for a person out of the provided details!
    """
    )
    col1, col2 = st.columns([1, 3])
    
    Prompt1 = (
        "Generate persona of doctor using information given in third person. \n---\n"
    )
    Prompt2 = (
        "Generate persona of doctor using information given in first person. \n---\n"
    )

    with col1:
        titles = st.selectbox('Title',('Dr.', 'Mrs.', 'Mr.', 'Ms.'))    
    with col2:
        name = st.text_input('Name') 
    name = "Name: " + titles + name + "\n"
    pronouns = st.selectbox("Pronouns",("-","He/Him", "She/Her", "They/Them"))
    pronouns = 'Pronouns: ' + pronouns +'\n'
    category = st.text_input("Category")
    category = "Category: " + category + "\n"
    speciality = st.text_input("Speciality")
    speciality = "Speciality: " + speciality + "\n"
    location = st.text_input("Location")
    location = "Location: " + location + "\n"
    keywords = st.text_input("Please enter few keywords (comma separated)")
    keywordsTemp = keywords
    keywords = "Keywords: " + keywords + "\n"
    hobbies = st.text_input("Hobbies")
    hobbies = "Hobbies: " + hobbies + "\n"
    education = st.text_input("Education")
    education = "Education: " + education + "\n"
    countries = st.text_input("Countries Visited")
    countries = "Countries visited: " + countries + "\n"
    passion = st.text_input("Passionate about")
    passion = "Passions: " + passion + "\n---\n"

    col3, col4 = st.columns([1.5, 1])

    def sugKey():
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt="Generate more keywords \n"+keywordsTemp,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )
        key =response['choices'][0]['text']
        return key
        
    with col3:
        keywords = st.text_input("Please enter few keywords (comma separated)")
        keywordsTemp = keywords
        keywords = "Keywords: " + keywords + "\n"
    
    with col4:
        if st.button("Suggest"):
            s = ''
            l = sugKey().split(',')
            rl = [i for i in l if i!= '']
            for i in rl:
                s += i
                s += ", "

            st.caption(s)
    
    Prompt = (
        Prompt1
        + name
        + category
        + speciality
        + location
        + keywords
        + hobbies
        + education
        + countries
        + passion
        + pronouns
    )
    Prompt_ = (
        Prompt2
        + name
        + category
        + speciality
        + location
        + keywords
        + hobbies
        + education
        + countries
        + passion
        + pronouns
    )

    option = st.selectbox(
        "Select the type of description",
        ("General (Suggested)", "Concise", "Stochastic"),
    )

    if st.button("Generate (Description)"):

        if (
            Prompt
            != "Generate persona of doctor using information given in third person. \n---\n"
            + "Name: "
            + "\n"
            + "Category: "
            + "\n"
            + "Speciality: "
            + "\n"
            + "Location: "
            + "\n"
            + "Keywords: "
            + "Hobbies: "
            + "\n"
            + "Education: "
            + "\n"
            + "Countries visited: "
            + "\n"
            + "Passions: "
            + "\n"
            + "Pronouns: "
            + "\n---"
            + "\n"
        ):

            openai.api_key_path = ".env"

            if option == "Concise":
                temperature = 0
                frequency_penalty = 2
                presence_penalty = 2

            if option == " Stochastic":
                temperature = 1
                frequency_penalty = 0
                presence_penalty = 0

            else:
                temperature = 0.8
                frequency_penalty = 1
                presence_penalty = 1

            def getdesc(Prompt):
                response = openai.Completion.create(
                    model="text-davinci-002",
                    prompt=Prompt,
                    temperature=temperature,
                    max_tokens=469,
                    top_p=1,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty,
                )

                desc = response["choices"][0]["text"]
                return desc
           
        else:
            st.write("Well, I am an AI but enter the details atleast")

        # st.write(Prompt)
        try:
            description = getdesc(Prompt)
            st.write(description)
                
            df = pd.DataFrame(
                {
                    "Bio": Prompt.replace(
                        "Generate persona of doctor using information given in third person. \n---\n ",
                        "",
                    ),
                    "Description": description,
                    "timestamp": datetime.datetime.utcnow(),
                },
                index=[0],
            )

            result = {
                "Bio": Prompt.replace(
                    "Generate persona of doctor using information given in third person. \n---\n ",
                    "",
                ),
                "Description": description,
                "timestamp": datetime.datetime.utcnow(),
            }

            df.to_csv("spry_desc.csv", mode="a", index=False, header=False)
            save_query(result)

        except:
            pass

        print("Done")

    if st.button("Generate (Bio)"):

        if (
            Prompt_
            != "Generate persona of doctor using information given in first person. \n---\n"
            + "Name: "
            + "\n"
            + "Category: "
            + "\n"
            + "Speciality: "
            + "\n"
            + "Location: "
            + "\n"
            + "Keywords: "
            + "Hobbies: "
            + "\n"
            + "Education: "
            + "\n"
            + "Countries visited: "
            + "\n"
            + "Passions: "
            + "\n"
            + "Pronouns: "
            + "\n---"
            + "\n"
        ):

            openai.api_key_path = ".env"

            if option == "Concise":
                temperature = 0
                frequency_penalty = 2
                presence_penalty = 2

            if option == " Stochastic":
                temperature = 1
                frequency_penalty = 0
                presence_penalty = 0

            else:
                temperature = 0.8
                frequency_penalty = 1
                presence_penalty = 1

            def getdesc(Prompt):
                response = openai.Completion.create(
                    model="text-davinci-002",
                    prompt=Prompt,
                    temperature=temperature,
                    max_tokens=469,
                    top_p=1,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty,
                )

                desc = response["choices"][0]["text"]
                return desc
   
        else:
            st.write("Well, I am an AI but enter the details atleast")

        # st.write(Prompt)

        try:
            description = getdesc(Prompt_)
            st.write(description)
                
            df = pd.DataFrame(
                {
                    "Bio": Prompt_.replace(
                        "Generate persona of doctor using information given in first person. \n---\n ",
                        "",
                    ),
                    "Description": description,
                    "timestamp": datetime.datetime.utcnow(),
                },
                index=[0],
            )

            df.to_csv("spry_desc.csv", mode="a", index=False, header=False)

            result = {
                "Bio": Prompt.replace(
                    "Generate persona of doctor using information given in first person. \n---\n ",
                    "",
                ),
                "Description": description,
                "timestamp": datetime.datetime.utcnow(),
            }

            save_query(result)
        except:
            pass

        print("Done")


def clinic():

    st.write(
        """
    # Clinic description writer
    This app can create a description for a clinic out of the provided details!
    """
    )

    Prompt1 = "Generate a description for a clinic \n---\n"

    name = st.text_input("Name")
    name = "Name: " + name + "\n"
    location = st.text_input("Location")
    location = "Location: " + location + "\n"
    facilities = st.text_input("Facilities")
    facilities = "Facilities: " + facilities + "\n"
    keywords = st.text_input("Please enter few keywords (comma separated)")
    keywords = "Keywords: " + keywords + "\n"

    Prompt = Prompt1 + name + location + facilities + keywords

    if st.button("Generate"):

        if (
            Prompt
            != "Generate a description for a clinic \n---\n"
            + "Name: "
            + "\n"
            + "Location: "
            + "\n"
            + "Facilities: "
            + "\n"
            + "Keywords: "
            + "\n"
        ):

            openai.api_key_path = ".env"

            def getdesc(Prompt):
                response = openai.Completion.create(
                    model="text-davinci-002",
                    prompt=Prompt,
                    temperature=0.8,
                    max_tokens=469,
                    top_p=1,
                    frequency_penalty=1,
                    presence_penalty=1,
                )

                desc = response["choices"][0]["text"]
                return desc

        else:
            st.write("Well, I am an AI but enter the details atleast")

        # st.write(Prompt)
        try:
            clinic = getdesc(Prompt)
            st.write(clinic)
            df = pd.DataFrame(
                {
                    "CLinic Details": Prompt.replace(
                        "Generate a description for a clinic \n---\n", ""
                    ),
                    "Description": clinic,
                },
                index=[0],
            )

            df.to_csv("spry_clinic.csv", mode="a", index=False, header=False)

            result = {
                "Clinic Details": Prompt.replace(
                    "Generate a description for a clinic \n---\n", ""
                ),
                "Description": clinic,
                "timestamp": datetime.datetime.utcnow(),
            }

            save_query(result)

        except:
            pass

        print("Done")


page_names_to_funcs = {
    "Home": main_page,
    "Blog Writer": blog,
    "Description writer": description,
    "Clinic Description": clinic,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
