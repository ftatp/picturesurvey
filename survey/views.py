from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from .models import Survey

import random
import os
import re
import json

# Create your views here.

def index(request):
	if request.method == 'POST':
		print(request.POST)
	
		subject_name = request.POST['name']
		subject_email = request.POST['email']
		
		sel_only5 = list(random.sample(range(18), 8))

		folderlist = [ dir for dir in os.listdir("static/instagram/") if os.path.isdir(os.path.join("static/instagram/", dir)) ]
		folderlist.sort()

		piclist = []
		for dirnum in range(18):
			if dirnum in sel_only5:
				selectnum = 5
			else:
				selectnum = 6

			dirname = folderlist[dirnum]
			
			filelist = [f for f in os.listdir('static/instagram/' + dirname)]

			rand_filelist = [ '../../static/instagram/' + dirname + '/' + filelist[i] for i in sorted(random.sample(range(len(filelist)), selectnum)) ]

			piclist += rand_filelist

	
		print("len: ", len(piclist))
		random.shuffle(piclist)
		piclist[0] = piclist[0][3:]
		picture_list = '|'.join(piclist)


		like_list = ""
		picture_count = 0
		like_count = 0
		caption = ""
		tag_list = ""

		picture_path = piclist[picture_count]

		picnum = re.findall(r'\d+', picture_path.split('/')[-1])
		picnum = int(picnum[0])

		with open("static/instagram/data" + str((int(picnum/100) + 1) * 100).zfill(4) + '.json') as jsonfile:
			data = json.load(jsonfile)
			
			for pic_explain in data['picture_list']:
				if str(picnum).zfill(4) in re.findall(r'\d+', pic_explain['path']):
					pattern = re.compile("\(\)")
					caption = re.sub(pattern, pic_explain['caption'])
					tag_list = ' '.join(pic_explain['tag_list'])

					break


		content = {
			'name': subject_name,
			'email': subject_email,
			'picture_list': picture_list,
			'like_list': like_list,
			'picture_count': picture_count,
			'like_count': like_count,
			'picture_path': picture_path,
			'caption': caption,
			'tag_list': tag_list
		}

		print(content)
		return render(request, 'picture_select.html', content)
	

	return render(request, 'index.html')


def picture_select(request):
	if request.method == 'POST':
		name = request.POST['name']
		email = request.POST['email']
		picture_list = request.POST['picture_list'].split('|')
		like_list = request.POST['like_list']
		picture_count = int(request.POST['picture_count'])
		like_count = int(request.POST['like_count'])
		picture_path = picture_list[picture_count]
			
		print("Path", picture_path)

		if "like" in request.POST.keys():
			like_list += "1 "
			like_count += 1
		else:
		 	like_list += "0 "

		if like_count == 36 or picture_count == 99:
			surveys = list(Survey.objects.all())

			id_code_list = [survey.id_code for survey in surveys]

			code = random.randint(1000,10000)
			while code in id_code_list:
				code = random.randint(1000,10000)

			picnum_list = [ picname.split('/')[-1] for picname in picture_list ]

			s = Survey(name=name, email=email, picture_list=picnum_list, like_list=like_list, id_code=code)
			s.save()
			
			context = {
				'id_code': code
			}

			template = loader.get_template('Done.html')
			return HttpResponse(template.render(context, request))
		else:
			caption = ""
			tag_list = ""

			picture_path = picture_list[picture_count]

			picnum = re.findall(r'\d+', picture_path.split('/')[-1])
			picnum = int(picnum[0])

			with open("static/instagram/data" + str((int(picnum/100) + 1) * 100).zfill(4) + '.json') as jsonfile:
				data = json.load(jsonfile)
				
				for pic_explain in data['picture_list']:
					if str(picnum).zfill(4) in re.findall(r'\d+', pic_explain['path']):
						pattern = re.compile("\(\)")
						caption = re.sub(pattern, '', pic_explain['caption'])
						tag_list = ' '.join(pic_explain['tag_list'])

						break

			picture_count += 1
			content = {
				'name': name,
				'email': email,
				'picture_list': '|'.join(picture_list),
				'like_list': like_list,
				'picture_count': picture_count,
				'like_count': like_count,
				'picture_path': picture_list[picture_count],
				'caption': caption,
				'tag_list': tag_list
			}
			
			print(content)
			return render(request, 'picture_select.html', content)

	else:
		return render(request, 'index.html')

def done(request):
	return render(request, 'Done.html')

