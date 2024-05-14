from pyecharts.charts import Geo
from pyecharts import options as opts

ROOT_PATH = 'https://echarts.apache.org/examples'
data = [
    [116.405289, 39.904987, 300],
    [121.472644, 31.231706, 200],
    [113.280637, 23.125178, 500],
    [113.894276, 22.9014, 100],
    [87.628704, 43.766717, 800]
]

data = [
    [coord[0], coord[1], coord[2]**0.5] for coord in data if coord[2] > 0
]

globe = (
    Geo(init_opts=opts.InitOpts(width="1600px", height="800px"))
    .add_schema(
        globe_opts=opts.GlobeOpts(
            environment=ROOT_PATH + '/data-gl/asset/starfield.jpg',
            height_texture=ROOT_PATH + '/data-gl/asset/bathymetry_bw_composite_4k.jpg',
            displacement_scale=0.05,
            displacement_quality='high',
            globe_outer_radius=100,
            base_color='#000',
            shading='realistic',
            realistic_material_opts=opts.RealisticMaterialOpts(
                roughness=0.2, metalness=0),
            post_effect_opts=opts.PostEffectOpts(enable=True, depth_of_field_opts=opts.DepthOfFieldOpts(
                focal_range=15, enable=True, focal_distance=100)),
            temporal_super_sampling_opts=opts.TemporalSuperSamplingOpts(
                enable=True),
            light_opts=opts.LightOpts(
                ambient_opts=opts.AmbientOpts(intensity=0),
                main_opts=opts.MainOpts(intensity=0.1, shadow=False),
                ambient_cubemap_opts=opts.AmbientCubemapOpts(
                    texture=ROOT_PATH + '/data-gl/asset/lake.hdr',
                    exposure=1,
                    diffuse_intensity=0.5,
                    specular_intensity=2
                )
            ),
            view_control_opts=opts.ViewControlOpts(
                auto_rotate=False,
                beta=180,
                alpha=20,
                distance=100
            )
        )
    )
    .add(
        series_name="",
        data_pair=data,
        type_=opts.ChartType.SCATTER3D,
        symbol_size=2,
        itemstyle_opts=opts.ItemStyleOpts(color="rgb(50, 50, 150)", opacity=1),
        blend_mode="lighter",
    )
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(is_show=False, min_=0, max_=60, range_color=[
                                          "#313695", "#4575b4", "#74add1", "#abd9e9", "#e0f3f8", "#ffffbf", "#fee090", "#fdae61", "#f46d43", "#d73027", "#a50026"]),
    )
)
globe.render("globe.html")
