"""Інтерактивні досліди; сервер запускається лише явною командою користувача."""
import matplotlib.pyplot as plt
import streamlit as st
import experiment1 as e1
import experiment2 as e2
import experiment3 as e3

st.set_page_config(page_title='Pseudo-Gaussian interpolation',layout='wide')
st.title('Псевдогаусова інтерполяція зі статті')
st.caption('Центри ядер фіксовані; авторська стратегія вибирає найближчі точки рівнів SDF=qΔ.')
page=st.sidebar.radio('Експеримент',['1. Ядро та стійкість','2. Геометрія та офсети','3. Параметри'])
def request_calculation():
    st.session_state['calculation_requested']=True


with st.sidebar:
    strategy=st.selectbox('Точки інтерполяції',['isolines','grid'],index=0)
    h=st.slider('Крок h',.16,.4,.24,.02,on_change=request_calculation)
    ratio=st.slider('Крок ізоліній Δ/h',.1,1.,.5,.05,on_change=request_calculation)
    rho=st.slider('ρ = r/h',.5,3.,2.,.1,on_change=request_calculation)
    order=st.slider('Порядок гладкості n',1,4,2,on_change=request_calculation)
    margin=st.checkbox('Граничний запас r',True)
    shape=st.selectbox('Форма',e2.SHAPES)
    angle=st.slider('Поворот, градуси',0.,90.,25.,5.,on_change=request_calculation)
    shift=st.slider('Зсув уздовж x',-.15,.15,.03,.01,on_change=request_calculation)
    offset=st.slider('Офсет t',-.6,.4,0.,.02,on_change=request_calculation)
    resolution=st.select_slider('Роздільність оцінки 2D / 3D',options=[31,51,71,101],value=51,on_change=request_calculation)
    surface=st.checkbox('Показати об’ємну ізоповерхню',True)
    submitted=st.button('Обчислити')
calculation_requested=st.session_state.pop('calculation_requested',False)
if submitted or calculation_requested:
    with st.spinner('Обчислення…'):
        try:
            if page.startswith('1'):
                result=e1.run(h=h,rho=rho,order=order,margin=margin,strategy=strategy,level_step=ratio*h)
                st.json(result[0],expanded=False);fig=e1.figure(result)
                st.pyplot(fig);plt.close(fig)
            else:
                res=min(resolution,51) if shape in ('sphere','torus') else resolution
                params=dict(shape=shape,h=h,rho=rho,order=order,angle=angle,shift=shift,
                            offset=offset,resolution=res,level_step=ratio*h,margin=margin)
                result=e2.run(**params,strategy=strategy)
                st.json(result[0],expanded=False);fig=e2.figure(result);st.pyplot(fig);plt.close(fig)
                # Контрольна стратегія має ту саму геометрію, центри й ядро.
                other=e2.run(**params,strategy='grid' if strategy=='isolines' else 'isolines')
                st.subheader('Порівняння за однакових умов')
                st.dataframe([result[0],other[0]])
                if shape in ('sphere','torus'):
                    if surface:
                        sf=e2.surface_figure(result);st.pyplot(sf);plt.close(sf)
                else:
                    cf=e2.comparison_figure([result,other]);st.pyplot(cf);plt.close(cf)
        except (RuntimeError,ValueError) as error:
            st.error(str(error))
if page.startswith('2'):
    st.info('Приклади 13×13 відтворюють описану конструкцію. Стаття не задає всіх параметрів для точного збігу рисунків.')
    if st.button('Приклади за схемою рисунків 4–6 та 8'):
        with st.spinner('Обчислення…'):
            cases=list(e2.paper_cases())
            st.dataframe([r[0] for r in cases])
            for start in range(0,len(cases),3):
                batch=cases[start:start+3]
                fig=e2.comparison_figure(batch);st.pyplot(fig);plt.close(fig)
if page.startswith('3'):
    st.write('Парні серії grid/isolines; включено Δ/h, сталий фізичний r та критичні офсети. Відмови зберігаються.')
    if st.button('Запустити повну серію'):
        with st.spinner('Серія експериментів…'):
            rows=e3.run_sweep();st.dataframe(rows);fig=e3.figure(rows);st.pyplot(fig);plt.close(fig)

if page.startswith('3'):
    if st.button('Добрати крок ізоліній: приклад за схемою рисунка 8'):
        with st.spinner('Калібрування кроку та незалежна перевірка…'):
            summary,trials,results=e3.optimize_level_step()
            st.json(summary,expanded=False);st.dataframe(trials)
            fig=e3.optimization_figure(summary,trials);st.pyplot(fig);plt.close(fig)
            fig=e2.comparison_figure(results);st.pyplot(fig);plt.close(fig)
            from storage import from_model
            import io
            archive=io.BytesIO();from_model(results[-1][-1]).save(archive)
            st.download_button('Завантажити готове поле (коефіцієнти)',archive.getvalue(),
                               file_name='optimized_field.npz',mime='application/octet-stream')
