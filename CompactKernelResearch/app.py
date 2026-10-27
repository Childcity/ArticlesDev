"""Запуск: streamlit run app.py. Змінюйте параметри й натискайте обчислення."""
import matplotlib.pyplot as plt
import streamlit as st
import experiment1 as e1
import experiment2 as e2
import experiment3 as e3

st.set_page_config(page_title='Compact kernel research',layout='wide')
st.title('Компактне ядро: три експерименти')
st.caption('Червоний контур — модель; чорний — точна SDF. Число компонент залежить від сітки оцінки.')
page=st.sidebar.radio('Експеримент',['1. Ядро та стійкість','2. Геометрія та офсети','3. Параметри'])
with st.sidebar.form('parameters'):
    h=st.slider('Крок h',.16,.4,.25,.02)
    rho=st.slider('ρ = r/h',.5,3.,2.,.1)
    order=st.slider('Порядок гладкості n',1,4,2)
    jitter=st.slider('Зміщення вузлів / h',0.,.3,0.,.025)
    margin=st.checkbox('Граничний запас r (експеримент 1)',True)
    shape=st.selectbox('Форма',e2.SHAPES)
    angle=st.slider('Поворот, градуси',0.,90.,25.,5.)
    shift=st.slider('Зсув уздовж x',-.15,.15,.03,.01)
    offset=st.slider('Офсет t',-.6,.4,0.,.02)
    resolution=st.select_slider('Роздільність оцінки 2D / 3D',options=[31,51,71,101],value=51)
    surface=st.checkbox('Показати об’ємну ізоповерхню',True)
    submitted=st.form_submit_button('Обчислити')
if submitted:
    with st.spinner('Обчислення…'):
        try:
            if page.startswith('1'):
                result=e1.run(h,rho,order,jitter,margin)
                st.json(result[0]);fig=e1.figure(result)
            elif page.startswith('2'):
                # Об'ємна оцінка обмежена 51^3, щоб інтерфейс залишався придатним для CPU.
                res=min(resolution,51) if shape in ('sphere','torus') else resolution
                result=e2.run(shape,h,rho,order,jitter,angle,shift,offset,res)
                st.json(result[0]);fig=e2.figure(result)
                if surface and shape in ('sphere','torus'):
                    sf=e2.surface_figure(result);st.pyplot(sf);plt.close(sf)
            else:
                result=e2.run(shape,h,rho,order,jitter,angle,shift,offset,min(resolution,51))
                st.json(result[0]);fig=e2.figure(result)
            st.pyplot(fig);plt.close(fig)
        except (RuntimeError,ValueError) as error:
            st.error(f'Обчислення не вдалося: {error}. Це може бути сингулярна конфігурація.')
if page.startswith('3'):
    st.write('Серія змінює по одному фактору. Окремо перевіряється сталий r=0.5 та критичні офсети.')
    if st.button('Запустити повну серію (CPU, кілька хвилин)'):
        with st.spinner('Серія експериментів…'):
            rows=e3.run_sweep();st.dataframe(rows);fig=e3.figure(rows);st.pyplot(fig);plt.close(fig)
