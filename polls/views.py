from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404

import csv
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np
from scipy import stats
from sklearn import datasets, linear_model
import re
import time
from datetime import*
from collections import*
from itertools import filterfalse
from plotly.offline import init_notebook_mode, iplot
from IPython.display import display, HTML
import plotly.offline as offline
import plotly.graph_objs as go
import pickle
import os

#import main1
from .main1 import course, student

from .models import course, student

class CustomUnpickler(pickle.Unpickler):

    def find_class(self, module, name):
        if name == 'Manager':
            from settings import Manager
            return Manager
        return super().find_class(module, name)

def data_to_plotly(x):
    k = []
    for i in range(0, len(x)):
        k.append(x[i][0])
    return k

def update_data(terms):
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    file0 = os.path.join(THIS_FOLDER, 'fall_winter_2018.file')
    with open(file0, "wb") as f:
        pickle.dump(terms, f, pickle.HIGHEST_PROTOCOL)
    #print("done updating terms")

def get_term(terms):
    term_list = ""
    print("Welcome to the PH20X course database.")
    print("The terms available are:")
    for l in range(len(terms)):
        term_list += terms[l].name
        if l < len(terms)-1:
            term_list += ", "
    print(term_list)
    while 1:
        selected_term = input("Please enter a term listed above:")
        for t in terms:
            print(t.name, selected_term)
            if t.name in selected_term:
                return t
        print("that is not a correct entry")

def create_new_act(term):
    act_name = input("Enter the dataset name.")
    search_by = input("Enter the dataset search parameter.")
    print("Your available graphs are:")
    print("aggrigate, median w/ 0's, median w/out 0's, scatter")
    plot = input("select one or type 'all'")
    if "agg" in plot:
        term.plot_agg(act_name,search_by)
        return
    elif "median w/ 0's" in plot:
        term.with_0s_medians_per_week(act_name,search_by)
        return
    elif "median w/out 0's" in plot:
        term.no_0s_medians_per_week(act_name,search_by)
        return
    elif "scatter" in plot:
        term.awesome_plot(act_name,search_by)
        return
    elif "all" in plot:
        term.plot_agg(act_name,search_by)
        term.with_0s_medians_per_week(act_name,search_by)
        term.no_0s_medians_per_week(act_name,search_by)
        term.awesome_plot(act_name,search_by)
        return

def get_activities(term):
    all = input("Do you want to combine some or all activities?")
    if "all" in all:
        return ["all"]
    elif "some" in all:
        datasets = term.check_activity(input("Enter each dataset and separate with a ' ' "))
        return datasets

def get_resp(term):
    while 1:
        act_list = get_activities(term)
        print("Your available graphs are:")
        print("aggrigate, median w/ 0's, median w/out 0's, scatter")
        plot = input("select one or type 'all'")
        if "agg" in plot:
            term.plot_agg(act_list)
            return
        elif "median w/ 0's" in plot:
            term.with_0s_medians_per_week(act_list)
            return
        elif "median w/out 0's" in plot:
            term.no_0s_medians_per_week(act_list)
            return
        elif "scatter" in plot:
            term.awesome_plot(act_list)
            return
        elif "all" in plot:
            term.plot_agg(act_list)
            term.with_0s_medians_per_week(act_list)
            term.no_0s_medians_per_week(act_list)
            term.awesome_plot(act_list)
            return

def load_files():
    #'spring','04/03/2017','06/15/2017'
    #'winter', '01/09/2017', '03/25/2017'
    #'fall','09/25/2016','12/11/2016'    doesnt include week 0
    f1 = course('Fall_2017','09/25/2017','12/11/2017')
    w1 = course('Winter_2018', '01/08/2018', '03/26/2018')
    #s1 = course('spring','04/03/2017','06/15/2017')

    #'ph201_F16_Anon_Grade.xlsx'
    #'ph202_w17_grades_boxsand-anon.xlsx'
    #'PH203-grade-book-deidentified.xlsx'
    #file0 = pd.read_excel('BoxSand_videos_Daily_Learning_Guide.xlsx')   #for later use in AI algorithm
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    file01 = os.path.join(THIS_FOLDER, 'ANON-ph201_f17_grades.xlsx')
    file02 = os.path.join(THIS_FOLDER, 'ANON-ph202_w18_grades.xlsx')
    file03 = os.path.join(THIS_FOLDER, 'ph201_f17_rawdata.xlsx')
    file04 = os.path.join(THIS_FOLDER, 'ph202_w18_rawdata.xlsx')

    file1 = pd.read_excel(file01)         #doesnt work for 202 due to 8 hw grades instead of 6
    file3 = pd.read_excel(file02)
    #file5 = pd.read_excel('PH203-grade-book-deidentified.xlsx')
    #file7 = pd.read_excel(file0,'PH 202 Winter 2017')           #imports duedates

    #'ph201_F16_Anon_BS_Data.xlsx'
    #'BoxSand-WS2017.xlsx'
    file2 = pd.read_excel(file03)
    file4 = pd.read_excel(file04)
    #file6 = pd.read_excel(file0,'PH 201 Fall 2016')             #imports duedates
    #file7 = pd.read_excel(file0,'PH 203 Spring 2017')           #imports duedates

    f1.add_students(file1, file2)
    w1.add_students(file3, file4)
    terms = [f1, w1]
    return terms
    #s1.add_students(file5, file4)
    #with open("fall_winter_2018.file", "wb") as f:
        #pickle.dump(terms, f, pickle.HIGHEST_PROTOCOL)
    #print("done loading file")

def retrieve_data():
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    file0 = os.path.join(THIS_FOLDER, 'fall_winter_2018.file')
    pickle_data = CustomUnpickler(open(file0, 'rb')).load()
    return pickle_data

def run():
    terms = retrieve_data()
    cont = 1
    while cont is 1:
        term = get_term(terms)
        activities = ""
        for l in range(len(term.activities)):
            activities += term.activities[l]
            if l < len(term.activities)-1:
                activities += ", "
        print("The currently available data sets are:")
        print(activities)
        response = input("Would you like to create a new dataset?")
        if "y" in response:
            create_new_act(term)
            update_data(terms)
        else:
            get_resp(term)
            update_data(terms)
        end_con = input("Do you wish to graph another activity?")
        if "n" in end_con:
            cont = 0

def bypass():
    terms = retrieve_data()
    f1 = terms[0]
    w1 = terms[1]

    #f1.with_0s_medians_per_week("Syllabus","Syllabus")
    #f1.no_0s_medians_per_week("Syllabus","Syllabus")
    #f1.plot_agg("Syllabus","Syllabus")
    f1.awesome_plot("Syllabus","Syllabus")
    w1.awesome_plot("Syllabus","Syllabus")
    update_data(terms)


# Create your views here.

def index(request):
    #main1.load_files()
    latest_course_list = retrieve_data()
    context = {'latest_course_list': latest_course_list}
    return render(request, 'polls/index.html', context)

def detail(request, course_id):
    #try:
    course_list = retrieve_data()
    for c in course_list:
        if c.name in course_id:
            return render(request, 'polls/detail.html', {'course': c})
    #courses = course.objects.get(pk=course_id)
    #except course.DoesNotExist:
    raise Http404("Course does not exist")


def results(request, course_id ,plot_id):
    course_list = retrieve_data()
    for c in course_list:
        if c.name in course_id:
            if "Agg_scatter" in plot_id:
                return render(request, "polls/Agg_scatter.html", {'course': c})
            elif "Scatter" in plot_id and not "Agg" in plot_id:
                return render(request, 'polls/Scatter.html', {'course': c})
            elif "Median_with_0's" in plot_id:
                return render(request, "polls/Median_with_0's.html", {'course': c})
            elif "Median_no_0's" in plot_id:
                return render(request, "polls/Median_no_0's.html", {'course': c})
            elif "Aggregate" in plot_id:
                return render(request, 'polls/Aggregate.html', {'course': c})
            raise Http404("Plot does not exist")
    raise Http404("Course does not exist")


def plot(request, course_id, plot_id, act_id):
    course_list = retrieve_data()
    for c in course_list:
        if c.name in course_id:
            file_name = c.name + "_" + course_id +"_" + plot_id + ".html"
            if "Agg_scatter" in plot_id:
                c.agg_scatter_plot(act_id)
                return render(request, "polls/Agg_scatter.html", {'course': c})
            elif "Scatter" in plot_id:
                c.awesome_plot(act_id)
                return render(request, "polls/Scatter.html", {'course': c})
            elif "Median_with_0's" in plot_id:
                c.with_0s_medians_per_week(act_id)
                return render(request, "polls/Median_with_0's.html", {'course': c})
            elif "Median_no_0's" in plot_id:
                c.no_0s_medians_per_week(act_id)
                return render(request, "polls/Median_no_0's.html", {'course': c})
            elif "Aggregate" in plot_id:
                c.plot_agg(act_id)
                return render(request, 'polls/Aggregate.html', {'course': c})

            raise Http404("Plot does not exist")
    raise Http404("Course does not exist")

def new_plot(request, course_id, plot_id, act_id, search_id):
    course_list = retrieve_data()
    for c in course_list:
        if c.name in course_id:
            if "delete" in act_id:
                c.del_activity(search_id)
                update_data(course_list)
                return render(request, 'polls/Scatter.html', {'course': c})
            c.new_activity(act_id, search_id)
            update_data(course_list)
            if "Agg_scatter" in plot_id:
                return render(request, "polls/Agg_scatter.html", {'course': c})
            elif "Scatter" in plot_id and not "Agg" in plot_id:
                return render(request, 'polls/Scatter.html', {'course': c})
            elif "Median_with_0's" in plot_id:
                return render(request, "polls/Median_with_0's.html", {'course': c})
            elif "Median_no_0's" in plot_id:
                return render(request, "polls/Median_no_0's.html", {'course': c})
            elif "Aggregate" in plot_id:
                return render(request, 'polls/Aggregate.html', {'course': c})
            raise Http404("Plot does not exist")
