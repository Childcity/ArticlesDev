"""Інтерактивний перегляд пунктів 4–6; важкі ресурсні серії запускаються CLI."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from comparators import CountedGeometry,build
from experiment4 import case
from quality import measure,gradient_quality
from core import sampling

OUT=Path(__file__).parent/'results'/'extended'


def read(name):return json.loads((OUT/(name+'.json')).read_text())


def show(page):
    if not (OUT/'summary.json').exists():
        st.info('Спочатку виконайте run_extended.py для відтворюваного добору та серій.');return
    st.caption('Параметри заморожено до перевірки. Медіани описові; цифрова топологія залежить від роздільності.')
    selected=read('selection')
    if page.startswith('4'):
        df=pd.DataFrame(read('holdout'))
        shape=st.selectbox('Незалежна форма',sorted(df['shape'].unique()))
        data=df[(df['shape']==shape)&(df['status']=='ok')]
        st.bar_chart(data.groupby('method')['band_rmse'].median())
        st.dataframe(data)
        st.subheader('Зафіксований добір і його вартість')
        st.json(selected)
    elif page.startswith('5'):
        with st.form('extended_quality'):
            shape=st.selectbox('Форма для перевірки',['capsule','rounded_box','neck','two_circles','sphere','torus'])
            method=st.selectbox('Метод',list(selected))
            resolution=st.select_slider('Роздільність витягування',options=[25,41,51,65,101,201],value=51)
            offset=st.slider('Офсет рівня',-.19,.34,0.,.01)
            submit=st.form_submit_button('Перевірити градієнти й топологію')
        if submit:
            dim=3 if shape in ('sphere','torus') else 2
            if dim==3 and resolution>65:
                st.info('Для інтерактивної 3D-перевірки використано 65³; більші серії запускайте CLI.');resolution=65
            with st.spinner('Обчислення…'):
                try:
                    g=CountedGeometry(**case(shape,42));model,info=build(method,g,h=.4 if dim==3 else .2,**selected[method]['config'])
                    st.dataframe(measure(model,g,resolution,(offset,)))
                    st.json(gradient_quality(model,g,dim,42))
                    axis,p=sampling(dim,resolution);truth=g(p).reshape([resolution]*dim);field=model.evaluate(p).reshape([resolution]*dim)
                    if dim==3:truth=truth[:,:,resolution//2];field=field[:,:,resolution//2]
                    fig,ax=plt.subplots(figsize=(5,4),layout='constrained')
                    for values,color in [(truth,'black'),(field,'red')]:
                        if values.min()<offset<values.max():ax.contour(axis,axis,values.T,levels=[offset],colors=color)
                    ax.set_aspect('equal');ax.set_title('Black: exact / red: model; 3D: z=0 slice')
                    st.pyplot(fig);plt.close(fig)
                except (ValueError,RuntimeError) as error:st.error(str(error))
    else:
        dim=st.selectbox('Розмірність',[2,3]);budget=st.select_slider('Серії по 8192 запити',options=[1,10,100],value=10)
        rows=[r for r in read('resources') if r['status']=='ok' and r['dim']==dim]
        for r in rows:
            r['total_for_budget']=r['total_seconds'][str(budget)]
            r['cached_edit_for_budget']=r.get('total_edit_seconds',{}).get(str(budget))
            r['peak_MiB']=r['peak_rss_bytes']/2**20
        df=pd.DataFrame(rows)
        st.scatter_chart(df,x='query_seconds',y='mean_offset_error',size='stored_bytes',color='method')
        st.dataframe(df)
        st.caption('Peak RSS включає імпорти; payload — лише дані поля. Cached edit утримує вихідні вузли, rebuild вибирає нові.')
        st.subheader('Карта порогових відмов (2D)')
        failures=pd.DataFrame(read('failure_map'))
        strategy=st.selectbox('Стратегія карти',['grid','isolines'])
        st.dataframe(failures[failures['strategy']==strategy])
