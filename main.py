import pandas as pd
import streamlit as st
from PIL import Image
import plotly.express as ex
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from template import book_template
how_many_books =None
filters= None

home = st.container()
visualisation = st.container()
about = st.container()
image = Image.open('BOOKS.jpg')
logo_im = Image.open('LOGO.png')

#### file reader, with st.cache, it makes data loading faster
@st.cache
def read_file(filename):
    df = pd.read_csv(filename,dtype=object)
    df.first_published = df.first_published.astype('int64')
    return df

####################### N a v b a r #################################
logo = st.sidebar.image(logo_im,width=100)

#dropdown menu as a navbar
selected = st.sidebar.selectbox('Navigation',('Home','Book Search','Data Visualization','About'))

#######################################################################
###################     H o m e   P a g e      ########################
#######################################################################
file1 = 'prepared_book.csv'
df1 = read_file(file1)
if selected == 'Home':
    with home:
        st.markdown('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">',unsafe_allow_html=True)
        st.markdown("""
                    <button type="button" class="btn btn-primary position-relative">
                        Home Page
                        <span class="position-absolute top-0 start-100 translate-middle p-2 bg-danger border border-light rounded-circle">
                            <span class="visually-hidden">New alerts</span>
                        </span>
                    </button>
                """,unsafe_allow_html=True)
        st.markdown("""<hr>""",unsafe_allow_html=True)

        st.write('\n'*10)
        st.subheader('The Best Epic Fantasy (fiction) - books collection')
        st.image(image,'Best epic fantasy books')
        


#######################################################################
####################### Data Visualisation page #######################
#######################################################################

elif selected == 'Book Search':
    st.markdown('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">',unsafe_allow_html=True)
    st.markdown("""
                    <button type="button" class="btn btn-primary position-relative">
                        Data Visualization Page
                        <span class="position-absolute top-0 start-100 translate-middle p-2 bg-danger border border-light rounded-circle">
                            <span class="visually-hidden">New alerts</span>
                        </span>
                    </button>
                """,unsafe_allow_html=True)
    st.markdown("""<hr>""",unsafe_allow_html=True)


####################### showing the list of books #####################
    
    #filtering and showing the book
    show_books = st.sidebar.checkbox('show the list of books') 
    if show_books:
        filtering = st.sidebar.checkbox('filter') 
        if filtering:
            left_col,mid_col,right_col = st.columns(3)
            filt_opt = left_col.selectbox('choose filter to search',('author','title','published year'))
            
            if filt_opt =='author':
                author_opt = mid_col.selectbox('pick author name:',df1.author.unique())
                df2 = df1[df1['author']==author_opt]
            elif filt_opt == 'published year':
                year_opt1 = mid_col.number_input('year min.',\
                        min_value = df1.first_published.min(),\
                        max_value = df1.first_published.max(),\
                        )
                year_opt2 = right_col.number_input('year max.',\
                        min_value = df1.first_published.min(),\
                        max_value = df1.first_published.max(),\
                        value = 2021
                        )
                df2 = df1[(df1['first_published']>=year_opt1) & (df1['first_published']<=year_opt2)]
            elif filt_opt == 'title':
                title_opt = mid_col.selectbox('pick title of the book :',df1.titles.unique())
                df2 = df1[df1['titles'] == title_opt]
            st.markdown("""<hr>""",unsafe_allow_html=True)

            
            col1,col2,col3 = st.columns(3)
            number_of_books = col1.metric('Number of books',df2.shape[0])
            number_of_authors = col2.metric('Number of author',df2['author'].nunique())
            years_range = col3.metric('Year range',f"{df2.first_published.min()}-{df2.first_published.max()}")
            st.markdown("""<hr>""",unsafe_allow_html=True)
            st.markdown('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">',unsafe_allow_html=True)
            ind_book = """
            <div class="card mb-3" style="max-width: 540px;">
                        <div class="row g-0">
                            <div class="col-md-4">
                            <img src={} class="img-fluid rounded-start" alt="...">
                            </div>
                            <div class="col-md-8">
                            <div class="card-body">
                                <h5 class="card-title">{}</h5>
                                <hr>
                                <ol>by {}</ol>
                                <ol><a href={} class="card-link">read on GoodReads</a></ol>
                            </ul>
                            </div>
                            </div>
                        </div>
                        </div>"""
            for i in range(df2.shape[0]):
                image_src = df2.iloc[i,:]['cover_url']
                book_title = df2.iloc[i,:]['titles']
                book_author = df2.iloc[i,:]['author']
                gr_url = df2.iloc[i,:]['url']
                st.markdown(ind_book.format(image_src,book_title,book_author,gr_url),unsafe_allow_html=True)
        
        raw_table = st.sidebar.checkbox('show whole list') 
        # user inputs the number of books using slider
        if raw_table:
            how_many_books = st.sidebar.slider('how many books to show',min_value=0,max_value=500,step=5)
            st.sidebar.markdown("""<hr>""",unsafe_allow_html=True)
            filter_opt = df1.columns
            filters = st.sidebar.multiselect('what do you want to show',filter_opt)
            if how_many_books:
                fig = go.Figure(data=[go.Table(
                    header = dict(values = filters,
                            fill_color='paleturquoise',
                            align = 'left'),
                    cells=dict(values = [df1[i].head(how_many_books) for i in df1[filters].columns],
                            fill_color='lavender',
                            align='left'
                )
            )])
                st.write(fig)
    
elif selected == 'Data Visualization':
    st.markdown('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">',unsafe_allow_html=True)
    st.markdown("""
                    <button type="button" class="btn btn-primary position-relative">
                        Data Visualization Page
                        <span class="position-absolute top-0 start-100 translate-middle p-2 bg-danger border border-light rounded-circle">
                            <span class="visually-hidden">New alerts</span>
                        </span>
                    </button>
                """,unsafe_allow_html=True)
    st.markdown("""<hr>""",unsafe_allow_html=True)
######################## data for charts #################################


    show_graphs = st.sidebar.checkbox('show graphs')

    if show_graphs:
        
        graph_opt = []
        figure_type = st.sidebar.multiselect('choose type of graph:',graph_opt)
        
        
     
        
     

   
    ######################################################################
    ##################      About Page        ############################
    ######################################################################
elif selected == 'About':
    team = st.container()
    tools = st.container()
    with about:
        st.markdown('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">',unsafe_allow_html=True)
        st.markdown("""
                    <button type="button" class="btn btn-primary position-relative">
                        About Page
                        <span class="position-absolute top-0 start-100 translate-middle p-2 bg-danger border border-light rounded-circle">
                            <span class="visually-hidden">New alerts</span>
                        </span>
                    </button>
                """,unsafe_allow_html=True)

        with team:
           st.subheader('Team')
           st.markdown("""
            ** Saidalikhon **- Data scraping / streamlit \n
            ** Sai **- Data visualization \n
            ** Sohan **- preprocessing \n
            ** Irene **- preprocessing \n
           """)
        with tools:
            st.subheader('Tools')
            st.markdown("""
                ** Streamlit **- creation of data app \n
                ** Plotly **- plotting / visualization \n
                ** Selenium **- data scraping  \n
                ** Pandas **- Data processing/analysis \n
            """)

        



