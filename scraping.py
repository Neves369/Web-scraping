import geopandas as gpd
import folium
import urllib.request
import pandas as pd
from bs4 import BeautifulSoup


def carregar_geojson(caminho):
    return gpd.read_file(caminho)


def filtrar_municipios(gdf, municipios):
    return gdf[gdf['name'].isin(municipios)]


def style_function(feature):
    return {
        'fillColor': '#00b4d8',
        'color': '#00b4d8',
        'weight': 2,
        'fillOpacity': 0.3
    }


def highlight_function(feature):
    return {
        'fillColor': '#0077b6',
        'color': '#0077b6',
        'weight': 3,
        'fillOpacity': 0.6
    }


def criar_mapa():
    return folium.Map(location=[-22.4165, -43.006], zoom_start=11)


def obter_informacoes_meteorologicas_ficticias(lat, lon):
    # Informações fictícias de clima
    temperatura = 25.0
    descricao = "Céu claro"
    umidade = 60
    return f"Temperatura: {temperatura}°C<br>Condição: {descricao}<br>Umidade: {umidade}%"


def adicionar_municipios_ao_mapa(gdf_filtrado, mapa):
    feature_group = folium.FeatureGroup(name="Informações dos Municípios")

    for _, municipio in gdf_filtrado.iterrows():
        nome = municipio['name']
        centroid = municipio['geometry'].centroid
        lat, lon = centroid.y, centroid.x

        clima_info = obter_informacoes_meteorologicas_ficticias(lat, lon)

        geo_json = folium.GeoJson(
            data=municipio['geometry'],
            name=nome,
            style_function=style_function,
            highlight_function=highlight_function,
        )

        geo_json.add_child(folium.Popup(
            f"{nome}<br>{clima_info}", max_width=300))

        folium.Marker(
            location=[centroid.y, centroid.x],
            icon=folium.DivIcon(
                html=f"<div style='font-size: 20px; color: #fff;'><b>{nome}</b></div>")
        ).add_to(mapa)

        feature_group.add_child(geo_json)

    # Adiciona ao mapa
    mapa.add_child(feature_group)


def adicionar_estacoes_ao_mapa(df, mapa):

    for index, row in df.iterrows():
        nome_estacao = row['Nome da Estação']
        # Teresópolis ------------------------------------
        if (nome_estacao == "Quebra Frascos"):
            lat = -22.417055130005
            lon = -43.007663726807
        elif (nome_estacao == "Comari"):
            lat = -22.445917129517
            lon = -42.975807189941
        elif (nome_estacao == "Posse - São Sebastião"):
            lat = -22.37310218811
            lon = -43.000965118408
        elif (nome_estacao == "Unifeso"):
            lat = -22.419393539429
            lon = -42.966999053955

        # Petrópolis -----------------------------------
        elif (nome_estacao == "Posse"):
            lat = -22.258111953735
            lon = -43.076362609863
        elif (nome_estacao == "Cuiabá"):
            lat = -22.379388809204
            lon = -43.067832946777
        elif (nome_estacao == "Itaipava"):
            lat = -22.405805587769
            lon = -43.10294342041
        elif (nome_estacao == "Itamarati"):
            lat = -22.484972000122
            lon = -43.150249481201
        elif (nome_estacao == "Araras"):
            lat = -22.434000015259
            lon = -43.255500793457
        elif (nome_estacao == "Barão do Rio Branco"):
            lat = -22.488166809082
            lon = -43.177665710449
        elif (nome_estacao == "LNCC"):
            lat = -22.530277252197
            lon = -43.217224121094
        elif (nome_estacao == "Bonfim"):
            lat = -22.461334228516
            lon = -43.095165252685
        else:
            lat, lon = -22.0 + index * 0.01, -43.0 + index * \
                0.01

        clima_info = obter_informacoes_meteorologicas_ficticias(lat, lon)

        # Adiciona marcador de estação no mapa
        folium.Marker(
            location=[lat, lon],
            popup=f"{nome_estacao}"
        ).add_to(mapa)


def adicionar_controle_de_camadas(mapa):
    folium.LayerControl().add_to(mapa)


def salvar_com_layout(mapa):
    mapa_html = mapa.get_root().render()

    layout_html = f"""
    <html>
        <head>
            <style>
                body {{
                    display: flex;
                    height: 100vh;
                    margin: 0;
                }}
                #map-container {{
                    flex: 1;  /* O mapa ocupa metade da tela */
                    height: 100%;
                }}
                #info-container {{
                    width: 300px;  /* A coluna tem 300px de largura */
                    background-color: #f4f4f4;
                    padding: 10px;
                    overflow-y: auto;
                    position: fixed;
                    top: 0;
                    left: 0;
                    height: 100%;
                    z-index: 999;
                }}
                #info-container h3 {{
                    margin-top: 0;
                    color: #0077b6;
                }}
                #info-container p {{
                    font-size: 16px;
                }}
            </style>
        </head>
        <body>
           
            <div id="map-container">
                {mapa_html}
            </div>

            <script>
                // Função para atualizar o conteúdo da coluna com o nome e informações do município
                function atualizarInformacoesMunicipio(nome, clima) {{
                    var infoContainer = document.getElementById("municipio-info");
                    infoContainer.innerHTML = "<b>" + nome + "</b><br>" + clima;
                }}

                // Agora, vamos garantir que o evento de clique no GeoJson funcione corretamente
                var map = L.map("map-container").setView([-22.4165, -43.006], 11);
                map.on("click", function(event) {{
                    var municipio_nome = event.target.feature && event.target.feature.properties.name;
                    if (municipio_nome) {{
                        var clima_info = "Temperatura: 25°C<br>Condição: Céu claro<br>Umidade: 60%";  // Informações fictícias
                        atualizarInformacoesMunicipio(
                            municipio_nome, clima_info);
                    }}
                }});
            </script>
        </body>
    </html>
    """

    with open("mapa.html", "w") as file:
        file.write(layout_html)
    print("Mapa criado ecom sucesso!")


def obter_dados_inea():
    # URL da página
    inea_url = "http://alertadecheias.inea.rj.gov.br/dados/piabanha.php"

    page = urllib.request.urlopen(inea_url)
    soup = BeautifulSoup(page, "html.parser")

    table_aba1 = soup.find('table', attrs={'class': 'TF'})  # Aba-1

    def processar_tabela(table):
        if not table:
            return pd.DataFrame()  # Retorna um DataFrame vazio se a tabela não existir
        a, b, c, d, e, f = [], [], [], [], [], []
        for row in table.findAll("tr"):  # para tudo que estiver em <tr>
            cells = row.findAll('td')  # variável para encontrar <td>
            if len(cells) == 17:  # número de colunas
                # iterando sobre cada linha
                a.append(cells[0].find(string=True))
                b.append(cells[1].find('a').string)
                c.append(cells[2].find(string=True))
                d.append(cells[3].find('img'))
                e.append(cells[4].find(string=True))
                f.append(cells[5].find(string=True))
        return pd.DataFrame({
            'Municipio': a,
            'Curso da Água': b,
            'Nome da Estação': c,
            'Status do Rio': d,
            'Última Leitura': e,
            'Status Monitoramento': f
        })

    # Processar a tabela
    df = processar_tabela(table_aba1)

    return df


def main():
    geojson_path = "geojs-33-mun.json"
    gdf = carregar_geojson(geojson_path)

    municipios_desejados = ['Teresópolis', 'Petrópolis']
    gdf_filtrado = filtrar_municipios(gdf, municipios_desejados)

    mapa = criar_mapa()

    adicionar_municipios_ao_mapa(gdf_filtrado, mapa)

    df_estacoes = obter_dados_inea()

    adicionar_estacoes_ao_mapa(df_estacoes, mapa)

    adicionar_controle_de_camadas(mapa)

    salvar_com_layout(mapa)


# Chamar a função principal
if __name__ == "__main__":
    main()
