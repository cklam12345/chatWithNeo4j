import time

import numpy as np 
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from neo4j_driver import run_query
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Medical Knowledge Worker Medical Assistant",
    page_icon="🧠",
    layout="wide",
)

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');
    </style>
    <div style='text-align: center; font-size: 2.5rem; font-weight: 600; font-family: "Roboto"; color: #018BFF; line-height:1; '>Hp Cool Medical Knowledge Worker Knowledge Graph Assistant</div>
    <div style='text-align: center; font-size: 1rem; font-weight: 300; font-family: "Roboto"; color: rgb(179 185 182); line-height:0; '>
        Powered by <svg width="80" height="60" xmlns="http://www.w3.org/2000/svg" id="Layer_1" data-name="Layer 1" viewBox="0 0 200 75"><path d="M39.23,19c-10.58,0-17.68,6.16-17.68,18.11v8.52A8,8,0,0,1,25,44.81a7.89,7.89,0,0,1,3.46.8V37.07c0-7.75,4.28-11.73,10.8-11.73S50,29.32,50,37.07V55.69h6.89V37.07C56.91,25.05,49.81,19,39.23,19Z"/><path d="M60.66,37.8c0-10.87,8-18.84,19.27-18.84s19.13,8,19.13,18.84v2.53H67.9c1,6.38,5.8,9.93,12,9.93,4.64,0,7.9-1.45,10-4.56h7.6c-2.75,6.66-9.27,10.94-17.6,10.94C68.63,56.64,60.66,48.67,60.66,37.8Zm31.15-3.62c-1.38-5.73-6.08-8.84-11.88-8.84S69.5,28.53,68.12,34.18Z"/><path d="M102.74,37.8c0-10.86,8-18.83,19.27-18.83s19.27,8,19.27,18.83-8,18.84-19.27,18.84S102.74,48.67,102.74,37.8Zm31.59,0c0-7.24-4.93-12.46-12.32-12.46S109.7,30.56,109.7,37.8,114.62,50.26,122,50.26,134.33,45.05,134.33,37.8Z"/><path d="M180.64,62.82h.8c4.42,0,6.08-2,6.08-7V20.16h6.89v35.2c0,8.84-3.48,13.4-12.32,13.4h-1.45Z"/><path d="M177.2,59.14h-6.89V50.65H152.86A8.64,8.64,0,0,1,145,46.2a7.72,7.72,0,0,1,.94-8.16L161.6,17.49a8.65,8.65,0,0,1,15.6,5.13V44.54h5.17v6.11H177.2ZM151.67,41.8a1.76,1.76,0,0,0-.32,1,1.72,1.72,0,0,0,1.73,1.73h17.23V22.45a1.7,1.7,0,0,0-1.19-1.68,2.36,2.36,0,0,0-.63-.09,1.63,1.63,0,0,0-1.36.73L151.67,41.8Z"/><path d="M191,5.53a5.9,5.9,0,1,0,5.89,5.9A5.9,5.9,0,0,0,191,5.53Z" fill="#018bff"/><path d="M24.7,47a5.84,5.84,0,0,0-3.54,1.2l-6.48-4.43a6,6,0,0,0,.22-1.59A5.89,5.89,0,1,0,9,48a5.81,5.81,0,0,0,3.54-1.2L19,51.26a5.89,5.89,0,0,0,0,3.19l-6.48,4.43A5.81,5.81,0,0,0,9,57.68a5.9,5.9,0,1,0,5.89,5.89A6,6,0,0,0,14.68,62l6.48-4.43a5.84,5.84,0,0,0,3.54,1.2A5.9,5.9,0,0,0,24.7,47Z" fill="#018bff"/></svg> | 
        <svg xmlns="http://www.w3.org/2000/svg" width="80" height="60" role="img" viewBox="103.32 268.82 893.36 274.86"><defs><clipPath id="a" clipPathUnits="userSpaceOnUse"><path d="M0 612h792V0H0z"/></clipPath></defs><g clip-path="url(#a)" transform="matrix(1.33333 0 0 -1.33333 0 816)"><path fill="#706d6e" d="M362.517 345.719l-3.45-9.662h-.188c-.607 2.275-1.637 5.475-3.24 9.557l-18.48 46.272h-18.014v-73.58h11.896v45.238c0 2.784-.07 6.165-.187 10.025-.047 1.959-.28 3.514-.34 4.702h.27a64.17 64.17 0 0 1 1.684-6.293l22.119-53.671h8.317l21.967 54.168c.478 1.228 1.028 3.638 1.508 5.796h.257c-.27-5.358-.526-10.246-.55-13.212v-46.752h12.668v73.579h-17.311z"/><path fill="#706d6e" d="M410.708 318.307h12.422v52.724h-12.422z"/><path fill="#706d6e" d="M417.048 393.441c-2.047 0-3.837-.69-5.287-2.07-1.474-1.38-2.211-3.123-2.211-5.164 0-2.024.737-3.726 2.187-5.082 1.45-1.34 3.24-2.012 5.31-2.012 2.083 0 3.873.672 5.347 2.012 1.45 1.356 2.198 3.058 2.198 5.082 0 1.976-.725 3.69-2.163 5.111-1.428 1.41-3.217 2.123-5.381 2.123"/><path fill="#706d6e" d="M467.04 371.568a34.198 34.198 0 0 1-6.948.737c-5.673 0-10.75-1.222-15.077-3.633-4.316-2.409-7.662-5.847-9.943-10.222-2.269-4.368-3.427-9.463-3.427-15.165 0-4.977 1.135-9.538 3.323-13.569 2.21-4.04 5.333-7.2 9.287-9.374 3.953-2.194 8.503-3.305 13.568-3.305 5.896 0 10.902 1.176 14.948 3.492l.188.094v11.375l-.526-.38a23.72 23.72 0 0 0-6.082-3.165c-2.189-.772-4.189-1.146-5.943-1.146-4.878 0-8.796 1.514-11.616 4.522-2.83 3-4.269 7.228-4.269 12.532 0 5.357 1.475 9.68 4.469 12.88 2.936 3.185 6.855 4.794 11.615 4.794 4.082 0 8.059-1.374 11.826-4.112l.526-.379v11.983l-.188.094c-1.415.79-3.356 1.444-5.731 1.947"/><path fill="#706d6e" d="M507.908 371.95c-3.135 0-5.918-1.002-8.292-2.967-2.105-1.737-3.614-4.117-4.773-7.07h-.128v9.117h-12.399v-52.724h12.4v26.968c0 4.603 1.028 8.357 3.087 11.205 2.001 2.813 4.713 4.241 8.024 4.241 1.111 0 2.351-.188 3.72-.556 1.343-.357 2.316-.76 2.888-1.17l.528-.374v12.51l-.188.093c-1.159.486-2.808.726-4.867.726"/><path fill="#706d6e" d="M551.468 331.706c-2.34-2.919-5.848-4.398-10.434-4.398-4.55 0-8.152 1.502-10.667 4.48-2.573 3-3.86 7.27-3.86 12.68 0 5.595 1.287 9.97 3.86 13.011 2.515 3.03 6.07 4.556 10.563 4.556 4.35 0 7.825-1.462 10.305-4.356 2.49-2.913 3.765-7.246 3.765-12.908 0-5.713-1.193-10.125-3.532-13.065m-9.896 40.61c-8.666 0-15.568-2.555-20.493-7.585-4.924-5.01-7.426-11.977-7.426-20.668 0-8.257 2.444-14.896 7.24-19.738 4.796-4.836 11.346-7.288 19.429-7.288 8.409 0 15.206 2.574 20.129 7.68 4.902 5.093 7.405 11.97 7.405 20.464 0 8.385-2.327 15.077-6.96 19.878-4.61 4.82-11.112 7.257-19.324 7.257"/><path fill="#706d6e" d="M595.367 349.251c-3.919 1.567-6.422 2.878-7.452 3.871-.994.971-1.497 2.328-1.497 4.054 0 1.537.61 2.754 1.92 3.765 1.286 1.001 3.075 1.503 5.32 1.503 2.105 0 4.258-.321 6.375-.976 2.106-.65 4-1.503 5.557-2.579l.503-.345v11.469l-.21.076c-1.405.626-3.324 1.152-5.616 1.585-2.293.421-4.398.632-6.187.632-5.93 0-10.82-1.515-14.539-4.493-3.768-2.999-5.685-6.935-5.685-11.702 0-2.48.42-4.667 1.228-6.533.82-1.871 2.081-3.527 3.766-4.913 1.637-1.368 4.2-2.801 7.616-4.264 2.865-1.174 4.982-2.163 6.35-2.952 1.333-.766 2.258-1.538 2.796-2.293.515-.749.784-1.748.784-2.988 0-3.551-2.656-5.275-8.106-5.275-2.035 0-4.352.421-6.878 1.251a26.352 26.352 0 0 0-7.03 3.567l-.526.38v-12.089l.188-.093c1.79-.825 4.022-1.514 6.678-2.041 2.631-.561 5.03-.831 7.087-.831 6.447 0 11.616 1.527 15.36 4.522 3.812 3.023 5.731 7.052 5.731 11.982 0 3.551-1.042 6.598-3.077 9.061-2.047 2.443-5.556 4.672-10.456 6.649"/><path fill="#706d6e" d="M652.12 331.706c-2.34-2.919-5.849-4.398-10.423-4.398-4.56 0-8.164 1.502-10.69 4.48-2.562 3-3.848 7.27-3.848 12.68 0 5.595 1.286 9.97 3.847 13.011 2.527 3.03 6.084 4.556 10.574 4.556 4.375 0 7.826-1.462 10.306-4.356 2.503-2.913 3.765-7.246 3.765-12.908 0-5.713-1.193-10.125-3.532-13.065m-9.872 40.61c-8.69 0-15.592-2.555-20.517-7.585-4.924-5.01-7.426-11.977-7.426-20.668 0-8.257 2.444-14.896 7.24-19.738 4.796-4.836 11.346-7.288 19.418-7.288 8.444 0 15.217 2.574 20.14 7.68 4.925 5.093 7.405 11.97 7.405 20.464 0 8.385-2.327 15.077-6.959 19.878-4.61 4.82-11.113 7.257-19.3 7.257"/><path fill="#706d6e" d="M734.652 360.924v10.106H722.09v15.733l-.42-.13-11.803-3.607-.235-.071V371.03h-18.609v6.645c0 3.093.701 5.456 2.047 7.035 1.368 1.556 3.3 2.345 5.767 2.345 1.765 0 3.614-.41 5.451-1.24l.456-.2v10.652l-.21.07c-1.72.63-4.06.936-6.985.936-3.66 0-6.982-.79-9.883-2.375-2.912-1.58-5.204-3.83-6.808-6.714-1.59-2.86-2.397-6.176-2.397-9.85v-7.304h-8.749v-10.106h8.75v-42.617h12.561v42.617h18.61V333.84c0-11.142 5.263-16.803 15.626-16.803 1.708 0 3.521.199 5.346.585 1.86.405 3.136.802 3.872 1.235l.175.093v10.217l-.503-.346c-.678-.443-1.544-.823-2.525-1.092-1.019-.286-1.837-.421-2.493-.421-2.432 0-4.223.649-5.334 1.935-1.146 1.31-1.707 3.585-1.707 6.785v24.896z"/><path fill="#f1511b" d="M173.559 308.824H90.737v82.84h82.822z"/><path fill="#80cc28" d="M264.999 308.824H182.16v82.84h82.839z"/><path fill="#00adef" d="M173.559 217.326H90.737v82.856h82.822z"/><path fill="#fbbc09" d="M264.999 217.326H182.16v82.856h82.839z"/><path fill="#706d6e" d="M360.488 246.929l-10.295 29.58c-.308.963-.636 2.515-.978 4.652h-.209c-.313-1.965-.657-3.514-1.037-4.652l-10.185-29.58zm23.422-28.907h-13.497l-6.67 18.876h-29.166l-6.41-18.876h-13.446l27.771 74.155h13.856z"/><path fill="#706d6e" d="M429.728 265.959l-28.593-38.578h28.489v-9.36h-45.298v4.5l29.217 39.092h-26.426v9.361h42.61z"/><path fill="#706d6e" d="M483.877 218.022H471.88v8.378h-.208c-3.483-6.413-8.894-9.62-16.236-9.62-12.513 0-18.772 7.515-18.772 22.546v31.647h11.997v-30.405c0-9.516 3.671-14.273 11.014-14.273 3.551 0 6.472 1.31 8.764 3.93 2.295 2.619 3.441 6.05 3.441 10.292v30.457h11.997z"/><path fill="#706d6e" d="M528.086 259.546c-1.447 1.138-3.53 1.705-6.253 1.705-3.552 0-6.515-1.601-8.894-4.81-2.38-3.204-3.567-7.564-3.567-13.082v-25.337h-11.998v52.952h11.998v-10.91h.203c1.17 3.723 2.973 6.627 5.405 8.71 2.432 2.087 5.145 3.13 8.144 3.13 2.17 0 3.827-.327 4.962-.983z"/><path fill="#706d6e" d="M566.77 249.72c-.036 4.31-1.052 7.663-3.052 10.058-1.999 2.395-4.754 3.595-8.273 3.595-3.447 0-6.369-1.26-8.764-3.774-2.395-2.52-3.869-5.812-4.42-9.88zm11.586-8.48H542.26c.135-4.894 1.646-8.67 4.525-11.325 2.88-2.656 6.832-3.981 11.867-3.981 5.655 0 10.842 1.687 15.564 5.066v-9.67c-4.827-3.032-11.206-4.55-19.13-4.55-7.796 0-13.904 2.406-18.336 7.214-4.43 4.809-6.644 11.576-6.644 20.298 0 8.238 2.437 14.952 7.316 20.14 4.88 5.19 10.941 7.783 18.18 7.783 7.236 0 12.84-2.327 16.808-6.98 3.963-4.655 5.946-11.12 5.946-19.391z"/></g></svg> <svg xmlns="http://www.w3.org/2000/svg" xmlns:v="https://vecta.io/nano" width="80" height="60" viewBox="0 0 338.667 83.339" fill="#0f0f0f"><path d="M200.154 32.427v.028c-.169 0-.339.028-.508.028s-.339-.028-.508-.028c-10.075 0-16.312 6.294-16.312 16.397v4.967c0 9.736 6.322 15.776 16.453 15.776a4.38 4.38 0 0 0 .621-.028c.141 0 .254.028.395.028 6.801 0 11.543-2.483 14.562-7.62l-6.011-3.472c-2.004 2.963-4.685 5.193-8.523 5.193-5.136 0-8.212-3.161-8.212-8.495V53.79h23.819v-5.87c0-9.426-6.18-15.494-15.776-15.494zm-.508 5.786c4.685.226 7.507 3.33 7.507 8.438v1.411h-15.07v-.819c0-5.644 2.681-8.805 7.563-9.031zm-36.998-5.758c-4.487 0-8.353 1.863-10.385 4.967l-.508.79v-4.911h-8.523v47.667h8.946v-16.65l.508.762c1.919 2.85 5.673 4.543 10.047 4.543h.226.197c7.366 0 14.788-4.798 14.788-15.55v-6.039c0-7.733-4.572-15.55-14.845-15.55l-.056-.028h-.197zm-2.088 6.717c5.193.085 8.41 3.612 8.41 9.257v5.192c0 5.644-3.246 9.144-8.495 9.257-4.882-.085-8.297-3.81-8.297-9.116v-5.334c0-5.362 3.443-9.144 8.382-9.257zm115.934-18.485l-17.215 48.09h9.68l3.302-10.301h18.795v.113l3.302 10.216h9.68l-17.243-48.09h-1.016l-.028-.028zm5.137 8.269l7.196 22.719h-14.45zm57.035-1.496v-6.773h-29.52v6.773h10.357v34.487h-10.357v6.773h29.52v-6.773h-10.357V27.46zm-97.139 4.996h-.254-.141c-4.995 0-8.551 1.693-10.301 4.939l-.536.988v-5.08h-8.523v35.446h8.946v-21.11c0-4.967 2.681-7.817 7.309-7.902 4.431.085 6.971 2.879 6.971 7.705v21.307h8.946V45.917c0-8.438-4.628-13.462-12.389-13.462zM114.473 19.699c-13.18 0-21.392 8.213-21.392 21.449v7.14c0 13.236 8.184 21.448 21.392 21.448h.198.197c13.18 0 21.392-8.212 21.392-21.448v-7.14c0-13.236-8.212-21.449-21.392-21.449h-.197zm.198 7.169c7.846.085 12.361 5.108 12.361 13.8v8.128c0 8.692-4.515 13.716-12.361 13.8-7.846-.085-12.362-5.108-12.362-13.8v-8.128c0-8.692 4.516-13.716 12.362-13.8zM36.751.001c-9.116 0-17.215 5.87-20.038 14.534A20.83 20.83 0 0 0 2.828 24.61C-1.744 32.512-.7 42.446 5.425 49.219 3.534 54.892 4.183 61.1 7.203 66.237c4.544 7.93 13.687 11.994 22.634 10.103a20.78 20.78 0 0 0 15.635 6.999c9.116 0 17.215-5.87 20.038-14.534 5.87-1.214 10.922-4.883 13.857-10.075 4.6-7.902 3.556-17.836-2.568-24.609v-.028a20.76 20.76 0 0 0-1.778-17.046C70.476 9.145 61.332 5.08 52.414 6.971A20.86 20.86 0 0 0 36.751.001zm0 5.419l-.028.028c3.669 0 7.197 1.27 10.019 3.613-.113.056-.339.197-.508.282L29.64 18.91c-.847.48-1.355 1.383-1.355 2.371v22.464l-7.14-4.12v-18.57A15.63 15.63 0 0 1 36.751 5.419zm19.99 6.54a15.62 15.62 0 0 1 13.566 7.825c1.806 3.161 2.483 6.858 1.862 10.442-.113-.085-.338-.197-.48-.282l-16.594-9.596a2.78 2.78 0 0 0-2.737 0L32.913 31.581V23.34l16.058-9.285a15.54 15.54 0 0 1 7.77-2.096zm-41.043 8.53v19.727c0 .988.508 1.863 1.355 2.371l19.416 11.204L29.3 57.94l-16.03-9.257a15.63 15.63 0 0 1-5.7-21.336 15.65 15.65 0 0 1 8.128-6.858zm37.196 4.882l16.058 9.257c7.479 4.318 10.018 13.857 5.7 21.336l.028.028c-1.834 3.161-4.713 5.588-8.128 6.83V43.095c0-.988-.508-1.891-1.355-2.37L45.753 29.492zm-11.797 6.802l8.185 4.741v9.454l-8.185 4.741-8.184-4.741v-9.454zm12.869 7.451l7.14 4.12v18.542c0 8.636-6.999 15.635-15.606 15.635v-.028c-3.641 0-7.197-1.27-9.991-3.612.113-.056.367-.198.508-.283l16.594-9.567c.847-.48 1.383-1.383 1.354-2.371zM49.309 51.76V60l-16.058 9.257c-7.479 4.29-17.018 1.75-21.336-5.701h.028c-1.834-3.133-2.484-6.858-1.863-10.442.113.085.339.197.48.282l16.594 9.596a2.78 2.78 0 0 0 2.737 0z"/></svg>
    </div>
""", unsafe_allow_html=True)

@st.cache_data
def get_data() -> pd.DataFrame:
    return run_query("""
      MATCH (n:Case) return n.id as Id, 
      n.summary as Summary ORDER BY Id""")

df_cases = get_data()
placeholder = st.empty()

with placeholder.container():
        df_diseases = run_query("""MATCH (n:Disease) return n.name as name""")
        df_body_systems = run_query("""MATCH (n:BodySystem) return n.name as name""")
        df_patients = run_query("""MATCH (n:Person) return n.id as name""")

        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric(
            label="Cases",
            value=len(df_cases)
        )
        kpi2.metric(
            label="Patients",
            value=len(df_patients)
        )
        kpi3.metric(
            label="Diseases",
            value=len(df_diseases)
        )    
        kpi4.metric(
            label="Body Systems",
            value=len(df_body_systems)
        )
    
        ep_team_col = st.columns(1)
        st.markdown("### Patients, Diseases & Affected Body Parts (Top N)")
        df_te_1 = run_query("""
            MATCH (e:BodySystem) 
            return e.id as id, e.name as label, '#33a02c' as color""")
        df_te_2 = run_query("""
            MATCH (t:Disease) 
            return t.id as id, t.name as label, '#1f78b4' as color""")
        df_te_3 = run_query("""
            MATCH (t:Person) 
            return t.id as id, t.id + ' (' + t.gender + ')' as label, '#fdbf6f' as color""")
        df_te = pd.concat([df_te_1, df_te_2], ignore_index=True)
        df_te = pd.concat([df_te, df_te_3], ignore_index=True)
        df_dis_bs = run_query("""
            MATCH (:Person)-[:HAS_DISEASE]->(d:Disease)-[a:AFFECTS]->(t:BodySystem)
            return DISTINCT t.id as source, d.id as target, count(a) as value, 
                '#a6cee3' as link_color LIMIT 50""")
        df_dis_patient = run_query(f"""
            MATCH (p:Person)-[:HAS_DISEASE]->(d:Disease)-[a:AFFECTS]->(t:BodySystem)
            WHERE t.id in [{','.join(f"'{x}'" for x in df_dis_bs['source'])}]
            return d.id as source, p.id as target, count(d) as value, 
                '#fdbf6f' as link_color LIMIT 50""")
        df_dis_bs_patient = pd.concat([df_dis_bs, df_dis_patient], ignore_index=True)
        label_mapping = dict(zip(df_te['id'], df_te.index))
        df_dis_bs_patient['src_id'] = df_dis_bs_patient['source'].map(label_mapping)
        df_dis_bs_patient['target_id'] = df_dis_bs_patient['target'].map(label_mapping)
        
        sankey = go.Figure(data=[go.Sankey(
            arrangement="snap",
            node = dict(
                pad = 15,
                thickness = 20,
                line = dict(
                    color = "black",
                    width = 0.4
                ),
                label = df_te['label'].values.tolist(),
                color = df_te['color'].values.tolist(),
                ),
            link = dict(
                source = df_dis_bs_patient['src_id'].values.tolist(),
                target = df_dis_bs_patient['target_id'].values.tolist(),
                value = df_dis_bs_patient['value'].values.tolist(),
                color = df_dis_bs_patient['link_color'].values.tolist()
            )
        )])
        st.plotly_chart(sankey, use_container_width=True)

        team_col = st.columns(1)
        st.markdown("### Top Symptoms")
        df_teams = run_query("""
            MATCH (e:Person)-[n:HAS_SYMPTOM]->(p:Symptom) 
              return DISTINCT p.description as symptom, count(n) as occurences
              ORDER BY occurences DESC LIMIT 10""")
        size_max_default = 7
        scaling_factor = 5
        fig_team = px.scatter(df_teams, x="symptom", y="occurences",
                    size="occurences", color="symptom",
                        hover_name="symptom", log_y=True, 
                        size_max=size_max_default*scaling_factor)
        st.plotly_chart(fig_team, use_container_width=True)

        # create two columns for charts
        fig_col1, fig_col2 = st.columns(2)
        with fig_col1:
            st.markdown("### Most Diagnoses")
            df = run_query("""
              MATCH (e:Person)-[:HAS_DIAGNOSIS]->(p:Diagnosis) 
              return DISTINCT p.name as diagnosis, count(e) as diagnoses
              ORDER BY diagnoses DESC LIMIT 10""")
            fig = px.scatter(df, x="diagnosis", y="diagnoses",
                      size="diagnoses", color="diagnosis",
                            hover_name="diagnosis", log_y=True, 
                            size_max=size_max_default*scaling_factor)
            st.plotly_chart(fig, use_container_width=True)
            
        with fig_col2:
            st.markdown("### Top Diseases")
            df = run_query("""
              MATCH (e:Person)-[:HAS_DISEASE]->(p:Disease) 
              return p.name as disease, count(e) as occurences
              ORDER BY occurences DESC LIMIT 10""")
            fig2 = px.scatter(df, x="disease", y="occurences",
                      size="occurences", color="disease",
                            hover_name="disease", log_y=True, 
                            size_max=size_max_default*scaling_factor)
            st.plotly_chart(fig2, use_container_width=True)
        
