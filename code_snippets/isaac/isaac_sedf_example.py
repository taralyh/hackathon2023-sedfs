

# %%
# Imports
import geopandas
import pandas as pd
from arcgis.features import GeoAccessor, GeoSeriesAccessor
from arcgis import GIS
import arcpy

from configuration_and_functions import *


# %%
bcgw_connection = r"W:\srm\sry\Workarea\isaacave\sedf_dataframes\bcgw_script.sde"
create_bcgw_connection(bcgw_connection, oracle_username, oracle_password)

# %%
# inputs
hackathon_gdb = r"W:\srm\sry\Workarea\isaacave\sedf_dataframes\hackathon2023_dataframes\Hackathon.gdb"

# from featureclass works with bcgw layers
vri_sdf = pd.DataFrame.spatial.from_featureclass(hackathon_gdb + "/s_vri2020_WolverineClip")
# vri_sdf.head()
fire_sdf = pd.DataFrame.spatial.from_featureclass(bcgw_connection + "/WHSE_LAND_AND_NATURAL_RESOURCE.PROT_HISTORICAL_FIRE_POLYS_SP")
WHA_sdf = pd.DataFrame.spatial.from_featureclass(bcgw_connection + "/WHSE_WILDLIFE_MANAGEMENT.WCP_WILDLIFE_HABITAT_AREA_POLY")

# %%
# Keep only the required fields
vri_sdf = vri_sdf[['PROJ_AGE_CLASS_CD_1', 'SPECIES_CD_1', 'FEATURE_AREA_SQM', 'SHAPE']]
fire_sdf = fire_sdf[['FIRE_DATE', 'FEATURE_AREA_SQM', 'SHAPE']]
WHA_sdf = WHA_sdf[['TAG', 'FEATURE_AREA_SQM', 'SHAPE']]

# Print columns, easier to see in interactive
# for column in vri_sdf.columns:
#     print(column)
# %%
# Intersecting
# This takes forever
fire_vri_sdf = vri_sdf.spatial.overlay(fire_sdf, op="intersection")
fire_vri_sdf = fire_vri_sdf.drop(columns = ["__idx2"]) # must drop field before next intersect
fire_vri_WHA_sdf = fire_vri_sdf.spatial.overlay(WHA_sdf, op="intersection")
fire_vri_WHA_sdf = fire_vri_WHA_sdf.drop(columns = ["__idx1", "__idx1_x", "__idx1_y", "__idx2", "FEATURE_AREA_SQM_1", "FEATURE_AREA_SQM_2", "FEATURE_AREA_SQM"])
# %%
# Area calc
fire_vri_WHA_sdf["area_ha"] = fire_vri_WHA_sdf.SHAPE.geom.area/10000
# %%
# Export result
fire_vri_WHA_sdf.spatial.to_featureclass(location=r"W:\srm\sry\Workarea\isaacave\sedf_dataframes\hackathon2023_dataframes\output.gdb/vri_fire_wha_intersect")

