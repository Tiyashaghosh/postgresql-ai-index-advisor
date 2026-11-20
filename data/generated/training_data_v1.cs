table,column,query_type,test_value,execution_time_before,execution_time_after,cost_before,cost_after,scan_before,scan_after,improvement_percent,value_frequency,table_rows,index_recommended
orders,customer_id,equality,1bd05d9a0031e8461d15550893d9b85a,9.916,0.017,3581.01,8.44,Seq Scan,Index Scan,99.83,1,99441,1
orders,customer_id,equality,596c05f5c6499d19b77e5e1c946116bf,9.124,0.088,3581.01,8.44,Seq Scan,Index Scan,99.04,1,99441,1
orders,customer_id,equality,654462019c31f990e4e83b074b585b0e,7.676,0.019,3581.01,8.44,Seq Scan,Index Scan,99.75,1,99441,1
orders,customer_id,equality,a486d2f4e67998e7c7e945dd4b801260,9.574,0.018,3581.01,8.44,Seq Scan,Index Scan,99.81,1,99441,1
orders,customer_id,equality,30ef3c7edfd9e0291574de45b6d59021,9.461,0.039,3581.01,8.44,Seq Scan,Index Scan,99.59,1,99441,1
orders,customer_id,equality,7ec2b3ab3c32f06c03da19590065fadb,9.183,0.035,3581.01,8.44,Seq Scan,Index Scan,99.62,1,99441,1
orders,customer_id,equality,f7dfccdce047cf62ddcfab87ac776e0d,9.487,0.019,3581.01,8.44,Seq Scan,Index Scan,99.8,1,99441,1
orders,customer_id,equality,27042fb514020b4fd8b981f6826d3b22,11.516,0.019,3581.01,8.44,Seq Scan,Index Scan,99.84,1,99441,1
orders,customer_id,equality,119e936a72d10c6ea12ab6129ffd9a79,9.88,0.016,3581.01,8.44,Seq Scan,Index Scan,99.84,1,99441,1
orders,customer_id,equality,5ad3e308b2ad8818e4f9f468c8949854,9.166,0.02,3581.01,8.44,Seq Scan,Index Scan,99.78,1,99441,1
orders,customer_id,equality,555c1dc901d3cae90a9d452d888865c5,9.726,0.073,3581.01,8.44,Seq Scan,Index Scan,99.25,1,99441,1
orders,customer_id,equality,84dbc8cadf81995826879280316b6397,9.45,0.018,3581.01,8.44,Seq Scan,Index Scan,99.81,1,99441,1
orders,order_status,equality,approved,7.97,0.035,3581.01,4.78,Seq Scan,Index Scan,99.56,2,99441,1
orders,order_status,equality,created,13.118,0.062,3581.01,10.89,Seq Scan,Index Scan,99.53,5,99441,1
orders,order_status,equality,processing,9.875,0.208,3581.01,134.43,Seq Scan,Index Scan,97.89,301,99441,1
orders,order_status,equality,invoiced,9.75,0.323,3581.01,139.77,Seq Scan,Index Scan,96.69,314,99441,1
orders,order_status,equality,unavailable,9.569,0.435,3581.01,267.47,Seq Scan,Index Scan,95.45,609,99441,1
orders,order_status,equality,canceled,9.459,0.373,3581.01,276.23,Seq Scan,Index Scan,96.06,625,99441,1
orders,order_status,equality,shipped,11.279,0.545,3581.01,440.3,Seq Scan,Index Scan,95.17,1107,99441,1
orders,order_status,equality,delivered,15.89,17.268,3581.01,3581.01,Seq Scan,Seq Scan,-8.67,96478,99441,0
order_items,product_id,equality,cfaace0475fb31c60cb29ff8abd131fe,5.321,0.021,3912.12,23.85,Seq Scan,Bitmap Heap Scan,99.61,1,112650,1
order_items,product_id,equality,1a20fafcc7f7eba192f047da438a0bb4,5.821,0.037,3912.12,23.85,Seq Scan,Bitmap Heap Scan,99.36,1,112650,1
order_items,product_id,equality,148c9e8af97e807544e4487f137ad65e,6.383,0.041,3912.12,23.85,Seq Scan,Bitmap Heap Scan,99.36,1,112650,1
order_items,product_id,equality,f1e06e6ee36f5c441232a96be23124f4,13.599,0.025,3912.12,23.85,Seq Scan,Bitmap Heap Scan,99.82,1,112650,1
order_items,product_id,equality,a5502e9954017124d95f7bce4c89d339,11.195,0.027,3912.12,23.85,Seq Scan,Bitmap Heap Scan,99.76,1,112650,1
order_items,product_id,equality,f54815785eb4b1d0fb3f5e81080694ff,6.329,0.023,3912.12,23.85,Seq Scan,Bitmap Heap Scan,99.64,1,112650,1
order_items,product_id,equality,10a96b8c9e62f372aaf40bf8ec897a75,5.583,0.035,3912.12,23.85,Seq Scan,Bitmap Heap Scan,99.37,1,112650,1
order_items,product_id,equality,8ce5f222608f6e18ea3b7acb84313c6b,7.503,0.026,3912.12,23.85,Seq Scan,Bitmap Heap Scan,99.65,2,112650,1
order_items,product_id,equality,ed647aab9859ee8a1e0dc6bdb6f4ba0b,5.878,0.029,3912.12,23.85,Seq Scan,Bitmap Heap Scan,99.51,2,112650,1
order_items,product_id,equality,146fed9eb1d0f9db43dad0c7c96fc6e8,6.656,0.028,3912.12,23.85,Seq Scan,Bitmap Heap Scan,99.58,4,112650,1
order_items,product_id,equality,b9900407a55cb2b306ae612415c3340e,7.186,0.058,3912.12,23.85,Seq Scan,Bitmap Heap Scan,99.19,6,112650,1
order_items,product_id,equality,75d6b6963340c6063f7f4cfcccfe6a30,10.04,0.112,3912.12,23.85,Seq Scan,Bitmap Heap Scan,98.88,93,112650,1
order_items,seller_id,equality,d93b8458c6fe139d85cfa5eadbf55bd2,8.189,0.054,3912.12,104.55,Seq Scan,Bitmap Heap Scan,99.34,1,112650,1
order_items,seller_id,equality,dd5450b022b2d00a2145a66331e1aef6,9.199,0.037,3912.12,104.55,Seq Scan,Bitmap Heap Scan,99.6,1,112650,1
order_items,seller_id,equality,9b00cad94ef3078faf6fba2e792c158f,6.568,0.037,3912.12,104.55,Seq Scan,Bitmap Heap Scan,99.44,1,112650,1
order_items,seller_id,equality,8e4f041ff58e7845456d3482524014b3,8.075,0.041,3912.12,104.55,Seq Scan,Bitmap Heap Scan,99.49,2,112650,1
order_items,seller_id,equality,52956b80ae65fda598f06f6b9943e7a9,7.533,0.028,3912.12,104.55,Seq Scan,Bitmap Heap Scan,99.63,3,112650,1
order_items,seller_id,equality,fc38b5dceee1a730fad8853453437fbd,5.42,0.042,3912.12,104.55,Seq Scan,Bitmap Heap Scan,99.23,5,112650,1
order_items,seller_id,equality,fe26f3ecb51a15e6d8335cd92da42562,7.075,0.031,3912.12,104.55,Seq Scan,Bitmap Heap Scan,99.56,7,112650,1
order_items,seller_id,equality,b5abf4f36adc043117b4fca82c22984c,5.659,0.03,3912.12,104.55,Seq Scan,Bitmap Heap Scan,99.47,12,112650,1
order_items,seller_id,equality,f4a04f7be452aa3bb31760bf00055dd0,6.567,0.053,3912.12,104.55,Seq Scan,Bitmap Heap Scan,99.19,18,112650,1
order_items,seller_id,equality,e96498ed8daaa3e9c23f7a62da76591c,6.829,0.058,3912.12,104.55,Seq Scan,Bitmap Heap Scan,99.15,34,112650,1
order_items,seller_id,equality,8cbac7e12637ed9cffa18c7875207478,8.57,0.065,3912.12,104.55,Seq Scan,Bitmap Heap Scan,99.24,82,112650,1
order_items,seller_id,equality,1f50f920176fa81dab994f9023523100,5.857,0.941,3912.12,2518.62,Seq Scan,Bitmap Heap Scan,83.93,1931,112650,1
products,product_category_name,equality,cds_dvds_musicais,1.783,0.023,964.89,11.97,Seq Scan,Bitmap Heap Scan,98.71,1,32951,1
products,product_category_name,equality,fashion_roupa_infanto_juvenil,1.888,0.024,964.89,22.96,Seq Scan,Bitmap Heap Scan,98.73,5,32951,1
products,product_category_name,equality,moveis_colchao_e_estofado,1.699,0.043,964.89,43.86,Seq Scan,Bitmap Heap Scan,97.47,10,32951,1
products,product_category_name,equality,musica,1.689,0.038,964.89,91.9,Seq Scan,Bitmap Heap Scan,97.75,27,32951,1
products,product_category_name,equality,moveis_quarto,1.81,0.046,964.89,146.71,Seq Scan,Bitmap Heap Scan,97.46,45,32951,1
products,product_category_name,equality,construcao_ferramentas_iluminacao,1.9,0.106,964.89,225.41,Seq Scan,Bitmap Heap Scan,94.42,78,32951,1
products,product_category_name,equality,moveis_cozinha_area_de_servico_jantar_e_jardim,1.842,0.079,964.89,257.33,Seq Scan,Bitmap Heap Scan,95.71,94,32951,1
products,product_category_name,equality,climatizacao,2.077,0.128,964.89,311.52,Seq Scan,Bitmap Heap Scan,93.84,124,32951,1
products,product_category_name,equality,consoles_games,2.035,0.182,964.89,503.48,Seq Scan,Bitmap Heap Scan,91.06,317,32951,1
products,product_category_name,equality,cool_stuff,1.868,0.405,964.89,601.35,Seq Scan,Bitmap Heap Scan,78.32,789,32951,1
products,product_category_name,equality,brinquedos,1.584,0.46,964.89,589.5,Seq Scan,Bitmap Heap Scan,70.96,1411,32951,1
products,product_category_name,equality,cama_mesa_banho,1.859,0.764,964.89,627.03,Seq Scan,Bitmap Heap Scan,58.9,3029,32951,1
customers,customer_state,equality,RR,4.814,0.05,2794.01,216.38,Seq Scan,Bitmap Heap Scan,98.96,46,99441,1
customers,customer_state,equality,AP,5.064,0.06,2794.01,206.99,Seq Scan,Bitmap Heap Scan,98.82,68,99441,1
customers,customer_state,equality,AC,6.185,0.101,2794.01,312.81,Seq Scan,Bitmap Heap Scan,98.37,81,99441,1
customers,customer_state,equality,TO,4.561,0.191,2794.01,677.28,Seq Scan,Bitmap Heap Scan,95.81,280,99441,1
customers,customer_state,equality,RN,4.81,0.282,2794.01,1058.46,Seq Scan,Bitmap Heap Scan,94.14,485,99441,1
customers,customer_state,equality,PB,5.446,0.317,2794.01,1058.46,Seq Scan,Bitmap Heap Scan,94.18,536,99441,1
customers,customer_state,equality,MT,5.449,0.56,2794.01,1424.75,Seq Scan,Bitmap Heap Scan,89.72,907,99441,1
customers,customer_state,equality,PE,4.401,0.801,2794.01,1659.3,Seq Scan,Bitmap Heap Scan,81.8,1652,99441,1
customers,customer_state,equality,ES,4.573,0.875,2794.01,1683.73,Seq Scan,Bitmap Heap Scan,80.87,2033,99441,1
customers,customer_state,equality,SC,7.194,1.431,2794.01,1642.74,Seq Scan,Bitmap Heap Scan,80.11,3637,99441,1
customers,customer_state,equality,MG,4.985,1.694,2794.01,1831.02,Seq Scan,Bitmap Heap Scan,66.02,11635,99441,1
customers,customer_state,equality,SP,7.941,6.217,2794.01,2544.16,Seq Scan,Bitmap Heap Scan,21.71,41746,99441,1
sellers,seller_state,equality,PA,0.215,0.016,74.69,8.3,Seq Scan,Index Scan,92.56,1,3095,1
sellers,seller_state,equality,MA,0.205,0.017,74.69,8.3,Seq Scan,Index Scan,91.71,1,3095,1
sellers,seller_state,equality,AM,0.207,0.013,74.69,8.3,Seq Scan,Index Scan,93.72,1,3095,1
sellers,seller_state,equality,AC,0.209,0.026,74.69,8.3,Seq Scan,Index Scan,87.56,1,3095,1
sellers,seller_state,equality,SE,0.24,0.037,74.69,10.91,Seq Scan,Bitmap Heap Scan,84.58,2,3095,1
sellers,seller_state,equality,MS,0.213,0.042,74.69,18.79,Seq Scan,Bitmap Heap Scan,80.28,5,3095,1
sellers,seller_state,equality,PE,0.291,0.027,74.69,25.15,Seq Scan,Bitmap Heap Scan,90.72,9,3095,1
sellers,seller_state,equality,BA,0.238,0.061,74.69,36.66,Seq Scan,Bitmap Heap Scan,74.37,19,3095,1
sellers,seller_state,equality,GO,0.265,0.056,74.69,42.8,Seq Scan,Bitmap Heap Scan,78.87,40,3095,1
sellers,seller_state,equality,RJ,0.252,0.088,74.69,43.74,Seq Scan,Bitmap Heap Scan,65.08,171,3095,1
sellers,seller_state,equality,MG,0.229,0.117,74.69,45.22,Seq Scan,Bitmap Heap Scan,48.91,244,3095,1
sellers,seller_state,equality,SP,0.478,0.358,74.69,74.69,Seq Scan,Seq Scan,25.1,1849,3095,1
orders,order_purchase_timestamp,range,2018-06-20 21:15:19 -> 2018-06-21 21:15:19,7.191,0.15,3829.61,615.01,Seq Scan,Bitmap Heap Scan,97.91,229,99441,1
orders,order_purchase_timestamp,range,2016-12-27 21:15:19 -> 2016-12-28 21:15:19,5.702,0.015,3829.61,31.32,Seq Scan,Bitmap Heap Scan,99.74,0,99441,1
orders,order_purchase_timestamp,range,2016-09-29 21:15:19 -> 2016-09-30 21:15:19,5.544,0.015,3829.61,31.32,Seq Scan,Bitmap Heap Scan,99.73,0,99441,1
orders,order_purchase_timestamp,range,2018-10-03 21:15:19 -> 2018-10-04 21:15:19,5.4,0.023,3829.61,68.37,Seq Scan,Bitmap Heap Scan,99.57,0,99441,1
orders,order_purchase_timestamp,range,2017-06-12 21:15:19 -> 2017-06-15 21:15:19,6.166,0.326,3829.61,885.15,Seq Scan,Bitmap Heap Scan,94.71,368,99441,1
orders,order_purchase_timestamp,range,2017-05-12 21:15:19 -> 2017-05-15 21:15:19,5.354,0.254,3829.61,940.15,Seq Scan,Bitmap Heap Scan,95.26,336,99441,1
orders,order_purchase_timestamp,range,2017-04-20 21:15:19 -> 2017-04-23 21:15:19,5.86,0.193,3829.61,773.36,Seq Scan,Bitmap Heap Scan,96.71,241,99441,1
orders,order_purchase_timestamp,range,2017-01-24 21:15:19 -> 2017-01-27 21:15:19,8.549,0.137,3829.61,79.25,Seq Scan,Bitmap Heap Scan,98.4,214,99441,1
orders,order_purchase_timestamp,range,2018-09-28 21:15:19 -> 2018-10-05 21:15:19,5.112,0.021,3829.61,399.82,Seq Scan,Bitmap Heap Scan,99.59,3,99441,1
orders,order_purchase_timestamp,range,2016-12-17 21:15:19 -> 2016-12-24 21:15:19,6.995,0.027,3829.61,173.49,Seq Scan,Bitmap Heap Scan,99.61,1,99441,1
orders,order_purchase_timestamp,range,2018-07-28 21:15:19 -> 2018-08-04 21:15:19,6.131,1.158,3829.61,2413.64,Seq Scan,Bitmap Heap Scan,81.11,1949,99441,1
orders,order_purchase_timestamp,range,2018-10-02 21:15:19 -> 2018-10-09 21:15:19,4.832,0.018,3829.61,396.8,Seq Scan,Bitmap Heap Scan,99.63,1,99441,1
orders,order_purchase_timestamp,range,2018-03-16 21:15:19 -> 2018-03-30 21:15:19,7.297,2.04,3829.61,2578.14,Seq Scan,Bitmap Heap Scan,72.04,3204,99441,1
orders,order_purchase_timestamp,range,2016-12-02 21:15:19 -> 2016-12-16 21:15:19,7.627,0.021,3829.61,323.02,Seq Scan,Bitmap Heap Scan,99.72,0,99441,1
orders,order_purchase_timestamp,range,2018-05-01 21:15:19 -> 2018-05-15 21:15:19,6.652,1.633,3829.61,2569.04,Seq Scan,Bitmap Heap Scan,75.45,3975,99441,1
orders,order_purchase_timestamp,range,2017-11-10 21:15:19 -> 2017-11-24 21:15:19,7.513,1.699,3829.61,2574.96,Seq Scan,Bitmap Heap Scan,77.39,3563,99441,1
orders,order_purchase_timestamp,range,2016-10-06 21:15:19 -> 2016-11-05 21:15:19,5.931,0.184,3829.61,625.92,Seq Scan,Bitmap Heap Scan,96.9,159,99441,1
orders,order_purchase_timestamp,range,2016-10-04 21:15:19 -> 2016-11-03 21:15:19,6.997,0.254,3829.61,628.63,Seq Scan,Bitmap Heap Scan,96.37,265,99441,1
orders,order_purchase_timestamp,range,2016-12-08 21:15:19 -> 2017-01-07 21:15:19,5.492,0.061,3829.61,623.2,Seq Scan,Bitmap Heap Scan,98.89,41,99441,1
orders,order_purchase_timestamp,range,2017-04-15 21:15:19 -> 2017-05-15 21:15:19,7.526,1.328,3829.61,2575.9,Seq Scan,Bitmap Heap Scan,82.35,3013,99441,1
orders,order_purchase_timestamp,range,2017-04-30 21:15:19 -> 2017-06-29 21:15:19,8.259,2.615,3829.61,2593.81,Seq Scan,Bitmap Heap Scan,68.34,6843,99441,1
orders,order_purchase_timestamp,range,2018-02-03 21:15:19 -> 2018-04-04 21:15:19,6.6,3.615,3829.61,2862.55,Seq Scan,Bitmap Heap Scan,45.23,14282,99441,1
orders,order_purchase_timestamp,range,2018-05-13 21:15:19 -> 2018-07-12 21:15:19,5.722,3.574,3829.61,2751.87,Seq Scan,Bitmap Heap Scan,37.54,11440,99441,1
orders,order_purchase_timestamp,range,2016-10-01 21:15:19 -> 2016-11-30 21:15:19,5.736,0.23,3829.61,1061.31,Seq Scan,Bitmap Heap Scan,95.99,324,99441,1
orders,order_purchase_timestamp,range,2018-04-01 21:15:19 -> 2018-06-30 21:15:19,8.248,4.585,3829.61,3069.31,Seq Scan,Bitmap Heap Scan,44.41,19792,99441,1
orders,order_purchase_timestamp,range,2017-03-26 21:15:19 -> 2017-06-24 21:15:19,6.008,3.455,3829.61,2672.93,Seq Scan,Bitmap Heap Scan,42.49,9137,99441,1
orders,order_purchase_timestamp,range,2018-07-01 21:15:19 -> 2018-09-29 21:15:19,7.48,3.583,3829.61,2785.73,Seq Scan,Bitmap Heap Scan,52.1,12690,99441,1
orders,order_purchase_timestamp,range,2018-03-16 21:15:19 -> 2018-06-14 21:15:19,11.473,4.567,3829.61,3061.65,Seq Scan,Bitmap Heap Scan,60.19,20154,99441,1
orders,order_purchase_timestamp,range,2017-11-07 21:15:19 -> 2018-03-07 21:15:19,6.211,6.605,3829.61,3347.71,Seq Scan,Bitmap Heap Scan,-6.34,28011,99441,0
orders,order_purchase_timestamp,range,2017-04-17 21:15:19 -> 2017-08-15 21:15:19,7.487,3.719,3829.61,2859.04,Seq Scan,Bitmap Heap Scan,50.33,14255,99441,1
orders,order_purchase_timestamp,range,2017-12-07 21:15:19 -> 2018-04-06 21:15:19,8.098,6.647,3829.61,3295.1,Seq Scan,Bitmap Heap Scan,17.92,26483,99441,0
orders,order_purchase_timestamp,range,2018-04-30 21:15:19 -> 2018-08-28 21:15:19,8.078,8.51,3829.61,3239.36,Seq Scan,Bitmap Heap Scan,-5.35,25843,99441,0
orders,order_purchase_timestamp,range,2017-06-15 21:15:19 -> 2017-12-12 21:15:19,12.614,8.309,3829.61,3402.42,Seq Scan,Bitmap Heap Scan,34.13,29198,99441,1
orders,order_purchase_timestamp,range,2016-09-10 21:15:19 -> 2017-03-09 21:15:19,7.477,2.897,3829.61,2575.54,Seq Scan,Bitmap Heap Scan,61.25,3651,99441,1
orders,order_purchase_timestamp,range,2017-02-14 21:15:19 -> 2017-08-13 21:15:19,6.229,4.284,3829.61,3009.34,Seq Scan,Bitmap Heap Scan,31.22,18561,99441,1
orders,order_purchase_timestamp,range,2017-11-10 21:15:19 -> 2018-05-09 21:15:19,8.252,12.43,3829.61,3829.61,Seq Scan,Seq Scan,-50.63,42407,99441,0
orders,order_purchase_timestamp,range,2017-02-25 21:15:19 -> 2017-11-22 21:15:19,6.888,9.637,3829.61,3549.06,Seq Scan,Bitmap Heap Scan,-39.91,33243,99441,0
orders,order_purchase_timestamp,range,2017-01-24 21:15:19 -> 2017-10-21 21:15:19,9.923,6.795,3829.61,3399.34,Seq Scan,Bitmap Heap Scan,31.52,30033,99441,1
orders,order_purchase_timestamp,range,2016-11-22 21:15:19 -> 2017-08-19 21:15:19,15.502,5.312,3829.61,3110.3,Seq Scan,Bitmap Heap Scan,65.73,21334,99441,1
orders,order_purchase_timestamp,range,2016-12-23 21:15:19 -> 2017-09-19 21:15:19,10.39,11.858,3829.61,3255.3,Seq Scan,Bitmap Heap Scan,-14.13,25741,99441,0
orders,order_purchase_timestamp,range,2017-09-29 21:15:19 -> 2018-09-29 21:15:19,15.678,10.272,3829.61,3829.61,Seq Scan,Seq Scan,34.48,71986,99441,1
orders,order_purchase_timestamp,range,2017-02-23 21:15:19 -> 2018-02-23 21:15:19,8.19,15.996,3829.61,3829.61,Seq Scan,Seq Scan,-95.31,55421,99441,0
orders,order_purchase_timestamp,range,2016-10-26 21:15:19 -> 2017-10-26 21:15:19,16.804,6.54,3829.61,3480.99,Seq Scan,Bitmap Heap Scan,61.08,31199,99441,1
orders,order_purchase_timestamp,range,2016-10-21 21:15:19 -> 2017-10-21 21:15:19,12.206,9.978,3829.61,3453.8,Seq Scan,Bitmap Heap Scan,18.25,30427,99441,0
orders,order_purchase_timestamp,range,2017-03-17 21:15:19 -> 2018-07-30 21:15:19,16.396,12.48,3829.61,3829.61,Seq Scan,Seq Scan,23.88,88176,99441,1
orders,order_purchase_timestamp,range,2016-10-23 21:15:19 -> 2018-03-07 21:15:19,15.333,15.971,3829.61,3829.61,Seq Scan,Seq Scan,-4.16,60849,99441,0
orders,order_purchase_timestamp,range,2017-03-06 21:15:19 -> 2018-07-19 21:15:19,18.887,15.668,3829.61,3829.61,Seq Scan,Seq Scan,17.04,86579,99441,0
orders,order_purchase_timestamp,range,2017-02-27 21:15:19 -> 2018-07-12 21:15:19,9.334,14.269,3829.61,3829.61,Seq Scan,Seq Scan,-52.87,85644,99441,0
orders,order_purchase_timestamp,range,2016-10-07 21:15:19 -> 2018-09-07 21:15:19,7.891,18.753,3829.61,3829.61,Seq Scan,Seq Scan,-137.65,99216,99441,0
orders,order_purchase_timestamp,range,2016-09-09 21:15:19 -> 2018-08-10 21:15:19,17.87,9.978,3829.61,3829.61,Seq Scan,Seq Scan,44.16,95936,99441,1
orders,order_purchase_timestamp,range,2016-11-01 21:15:19 -> 2018-10-02 21:15:19,15.559,17.515,3829.61,3829.61,Seq Scan,Seq Scan,-12.57,99110,99441,0
orders,order_purchase_timestamp,range,2016-11-11 21:15:19 -> 2018-10-12 21:15:19,15.557,16.23,3829.61,3829.61,Seq Scan,Seq Scan,-4.33,99111,99441,0
orders,order_delivered_customer_date,range,2017-02-15 13:46:32 -> 2017-02-16 13:46:32,11.367,0.105,3829.61,180.25,Seq Scan,Bitmap Heap Scan,99.08,96,99441,1
orders,order_delivered_customer_date,range,2017-11-02 13:46:32 -> 2017-11-03 13:46:32,11.876,0.034,3829.61,441.61,Seq Scan,Bitmap Heap Scan,99.71,19,99441,1
orders,order_delivered_customer_date,range,2016-12-30 13:46:32 -> 2016-12-31 13:46:32,10.377,0.029,3829.61,35.09,Seq Scan,Bitmap Heap Scan,99.72,0,99441,1
orders,order_delivered_customer_date,range,2018-04-29 13:46:32 -> 2018-04-30 13:46:32,14.796,0.041,3829.61,537.09,Seq Scan,Bitmap Heap Scan,99.72,35,99441,1
orders,order_delivered_customer_date,range,2017-08-07 13:46:32 -> 2017-08-10 13:46:32,8.241,0.366,3829.61,889.98,Seq Scan,Bitmap Heap Scan,95.56,538,99441,1
orders,order_delivered_customer_date,range,2018-07-16 13:46:32 -> 2018-07-19 13:46:32,7.758,0.08,3829.61,806.22,Seq Scan,Bitmap Heap Scan,98.97,58,99441,1
orders,order_delivered_customer_date,range,2018-07-06 13:46:32 -> 2018-07-09 13:46:32,15.055,0.326,3829.61,1324.84,Seq Scan,Bitmap Heap Scan,97.83,303,99441,1
orders,order_delivered_customer_date,range,2017-10-16 13:46:32 -> 2017-10-19 13:46:32,10.554,0.686,3829.61,1125.14,Seq Scan,Bitmap Heap Scan,93.5,641,99441,1
orders,order_delivered_customer_date,range,2018-05-25 13:46:32 -> 2018-06-01 13:46:32,11.543,0.589,3829.61,1880.92,Seq Scan,Bitmap Heap Scan,94.9,488,99441,1
orders,order_delivered_customer_date,range,2017-04-25 13:46:32 -> 2017-05-02 13:46:32,10.124,0.188,3829.61,1000.1,Seq Scan,Bitmap Heap Scan,98.14,255,99441,1
orders,order_delivered_customer_date,range,2018-10-02 13:46:32 -> 2018-10-09 13:46:32,12.534,0.015,3829.61,444.56,Seq Scan,Bitmap Heap Scan,99.88,0,99441,1
orders,order_delivered_customer_date,range,2016-12-21 13:46:32 -> 2016-12-28 13:46:32,9.963,0.015,3829.61,203.71,Seq Scan,Bitmap Heap Scan,99.85,0,99441,1
orders,order_delivered_customer_date,range,2016-11-26 13:46:32 -> 2016-12-10 13:46:32,8.694,0.035,3829.61,375.54,Seq Scan,Bitmap Heap Scan,99.6,2,99441,1
orders,order_delivered_customer_date,range,2018-08-19 13:46:32 -> 2018-09-02 13:46:32,12.117,2.158,3829.61,2537.78,Seq Scan,Bitmap Heap Scan,82.19,3553,99441,1
orders,order_delivered_customer_date,range,2017-06-01 13:46:32 -> 2017-06-15 13:46:32,11.777,0.789,3829.61,2188.07,Seq Scan,Bitmap Heap Scan,93.3,1417,99441,1
orders,order_delivered_customer_date,range,2017-08-03 13:46:32 -> 2017-08-17 13:46:32,9.711,1.153,3829.61,2399.66,Seq Scan,Bitmap Heap Scan,88.13,1853,99441,1
orders,order_delivered_customer_date,range,2016-12-31 13:46:32 -> 2017-01-30 13:46:32,8.919,0.188,3829.61,708.73,Seq Scan,Bitmap Heap Scan,97.89,221,99441,1
orders,order_delivered_customer_date,range,2017-06-06 13:46:32 -> 2017-07-06 13:46:32,9.308,1.873,3829.61,2577.84,Seq Scan,Bitmap Heap Scan,79.88,3166,99441,1
orders,order_delivered_customer_date,range,2017-01-22 13:46:32 -> 2017-02-21 13:46:32,11.596,0.658,3829.61,1541.62,Seq Scan,Bitmap Heap Scan,94.33,1278,99441,1
orders,order_delivered_customer_date,range,2017-11-04 13:46:32 -> 2017-12-04 13:46:32,10.801,1.177,3829.61,2523.47,Seq Scan,Bitmap Heap Scan,89.1,4697,99441,1
orders,order_delivered_customer_date,range,2017-07-22 13:46:32 -> 2017-09-20 13:46:32,10.743,1.504,3829.61,2632.13,Seq Scan,Bitmap Heap Scan,86.0,8018,99441,1
orders,order_delivered_customer_date,range,2018-01-18 13:46:32 -> 2018-03-19 13:46:32,13.95,4.091,3829.61,2812.18,Seq Scan,Bitmap Heap Scan,70.67,12814,99441,1
orders,order_delivered_customer_date,range,2018-07-23 13:46:32 -> 2018-09-21 13:46:32,10.706,5.675,3829.61,2705.75,Seq Scan,Bitmap Heap Scan,46.99,10904,99441,1
orders,order_delivered_customer_date,range,2017-10-19 13:46:32 -> 2017-12-18 13:46:32,8.254,4.006,3829.61,2745.75,Seq Scan,Bitmap Heap Scan,51.47,10720,99441,1
orders,order_delivered_customer_date,range,2017-03-26 13:46:32 -> 2017-06-24 13:46:32,6.865,3.811,3829.61,2652.76,Seq Scan,Bitmap Heap Scan,44.49,8679,99441,1
orders,order_delivered_customer_date,range,2017-10-25 13:46:32 -> 2018-01-23 13:46:32,7.502,4.834,3829.61,2961.8,Seq Scan,Bitmap Heap Scan,35.56,17225,99441,1
orders,order_delivered_customer_date,range,2017-10-09 13:46:32 -> 2018-01-07 13:46:32,12.416,4.748,3829.61,2946.06,Seq Scan,Bitmap Heap Scan,61.76,16415,99441,1
orders,order_delivered_customer_date,range,2017-05-13 13:46:32 -> 2017-08-11 13:46:32,7.367,4.755,3829.61,2736.37,Seq Scan,Bitmap Heap Scan,35.46,10614,99441,1
orders,order_delivered_customer_date,range,2017-07-11 13:46:32 -> 2017-11-08 13:46:32,10.636,5.925,3829.61,2911.89,Seq Scan,Bitmap Heap Scan,44.29,16231,99441,1
orders,order_delivered_customer_date,range,2016-12-23 13:46:32 -> 2017-04-22 13:46:32,7.319,1.665,3829.61,2518.8,Seq Scan,Bitmap Heap Scan,77.25,5629,99441,1
orders,order_delivered_customer_date,range,2017-04-04 13:46:32 -> 2017-08-02 13:46:32,13.439,3.966,3829.61,2791.53,Seq Scan,Bitmap Heap Scan,70.49,12316,99441,1
orders,order_delivered_customer_date,range,2018-04-10 13:46:32 -> 2018-08-08 13:46:32,9.036,6.293,3829.61,3310.05,Seq Scan,Bitmap Heap Scan,30.36,26932,99441,1
orders,order_delivered_customer_date,range,2017-06-18 13:46:32 -> 2017-12-15 13:46:32,10.702,8.399,3829.61,3271.64,Seq Scan,Bitmap Heap Scan,21.52,26051,99441,1
orders,order_delivered_customer_date,range,2017-03-27 13:46:32 -> 2017-09-23 13:46:32,12.982,5.38,3829.61,3058.36,Seq Scan,Bitmap Heap Scan,58.56,20101,99441,1
orders,order_delivered_customer_date,range,2018-01-27 13:46:32 -> 2018-07-26 13:46:32,7.543,9.021,3829.61,3767.1,Seq Scan,Bitmap Heap Scan,-19.59,39893,99441,0
orders,order_delivered_customer_date,range,2017-11-03 13:46:32 -> 2018-05-02 13:46:32,9.902,13.81,3829.61,3747.85,Seq Scan,Bitmap Heap Scan,-39.47,38863,99441,0
orders,order_delivered_customer_date,range,2017-02-26 13:46:32 -> 2017-11-23 13:46:32,17.78,10.542,3829.61,3428.06,Seq Scan,Bitmap Heap Scan,40.71,30390,99441,1
orders,order_delivered_customer_date,range,2017-09-03 13:46:32 -> 2018-05-31 13:46:32,11.524,16.017,3829.61,3829.61,Seq Scan,Seq Scan,-38.99,54374,99441,0
orders,order_delivered_customer_date,range,2017-09-28 13:46:32 -> 2018-06-25 13:46:32,16.274,14.969,3829.61,3829.61,Seq Scan,Seq Scan,8.02,56262,99441,0
orders,order_delivered_customer_date,range,2017-07-23 13:46:32 -> 2018-04-19 13:46:32,17.249,16.777,3829.61,3829.61,Seq Scan,Seq Scan,2.74,50102,99441,0
orders,order_delivered_customer_date,range,2017-01-31 13:46:32 -> 2018-01-31 13:46:32,15.103,15.957,3829.61,3829.61,Seq Scan,Seq Scan,-5.65,46995,99441,0
orders,order_delivered_customer_date,range,2017-09-26 13:46:32 -> 2018-09-26 13:46:32,8.992,14.553,3829.61,3829.61,Seq Scan,Seq Scan,-61.84,72326,99441,0
orders,order_delivered_customer_date,range,2017-03-26 13:46:32 -> 2018-03-26 13:46:32,11.21,15.36,3829.61,3829.61,Seq Scan,Seq Scan,-37.02,55277,99441,0
orders,order_delivered_customer_date,range,2016-11-08 13:46:32 -> 2017-11-08 13:46:32,12.594,7.004,3829.61,3418.66,Seq Scan,Bitmap Heap Scan,44.39,29997,99441,1
orders,order_delivered_customer_date,range,2016-12-08 13:46:32 -> 2018-04-22 13:46:32,14.499,8.362,3829.61,3829.61,Seq Scan,Seq Scan,42.33,65870,99441,1
orders,order_delivered_customer_date,range,2017-05-09 13:46:32 -> 2018-09-21 13:46:32,18.645,18.625,3829.61,3829.61,Seq Scan,Seq Scan,0.11,89573,99441,0
orders,order_delivered_customer_date,range,2016-10-19 13:46:32 -> 2018-03-03 13:46:32,15.091,15.276,3829.61,3829.61,Seq Scan,Seq Scan,-1.23,54117,99441,0
orders,order_delivered_customer_date,range,2017-05-05 13:46:32 -> 2018-09-17 13:46:32,13.472,10.345,3829.61,3829.61,Seq Scan,Seq Scan,23.21,89918,99441,1
orders,order_delivered_customer_date,range,2016-10-31 13:46:32 -> 2018-10-01 13:46:32,16.551,11.429,3829.61,3829.61,Seq Scan,Seq Scan,30.95,96276,99441,1
orders,order_delivered_customer_date,range,2016-11-05 13:46:32 -> 2018-10-06 13:46:32,12.945,16.906,3829.61,3829.61,Seq Scan,Seq Scan,-30.6,96248,99441,0
orders,order_delivered_customer_date,range,2016-10-28 13:46:32 -> 2018-09-28 13:46:32,8.802,19.071,3829.61,3829.61,Seq Scan,Seq Scan,-116.67,96296,99441,0
orders,order_delivered_customer_date,range,2016-10-15 13:46:32 -> 2018-09-15 13:46:32,14.181,17.404,3829.61,3829.61,Seq Scan,Seq Scan,-22.73,96419,99441,0
customers,customer_state,in,"RR, AP",12.854,0.111,2794.01,317.11,Seq Scan,Bitmap Heap Scan,99.14,114,99441,1
customers,customer_state,in,"RR, AP, AC",15.301,0.164,2918.31,481.54,Seq Scan,Bitmap Heap Scan,98.93,195,99441,1
customers,customer_state,in,"GO, ES",12.6,1.928,2794.01,1650.35,Seq Scan,Bitmap Heap Scan,84.7,4053,99441,1
customers,customer_state,in,"GO, ES, DF",14.972,2.5,2918.31,1709.34,Seq Scan,Bitmap Heap Scan,83.3,6193,99441,1
customers,customer_state,in,"RR, AP, GO, ES",10.088,1.703,3042.61,1662.52,Seq Scan,Bitmap Heap Scan,83.12,4167,99441,1
sellers,seller_state,in,"PI, AM",0.332,0.04,74.69,15.19,Seq Scan,Bitmap Heap Scan,87.95,2,3095,1
sellers,seller_state,in,"PI, AM, PA",0.44,0.03,78.56,18.02,Seq Scan,Bitmap Heap Scan,93.18,3,3095,1
sellers,seller_state,in,"BA, ES",0.321,0.039,74.69,47.26,Seq Scan,Bitmap Heap Scan,87.85,42,3095,1
sellers,seller_state,in,"BA, ES, DF",0.38,0.078,78.56,46.11,Seq Scan,Bitmap Heap Scan,79.47,72,3095,1
sellers,seller_state,in,"PI, AM, BA, ES",0.462,0.071,82.42,47.48,Seq Scan,Bitmap Heap Scan,84.63,44,3095,1
orders,order_status,in,"approved, created",14.631,0.024,3581.01,15.53,Seq Scan,Index Scan,99.84,7,99441,1
orders,order_status,in,"approved, created, processing",12.601,0.24,3705.31,165.47,Seq Scan,Index Scan,98.1,308,99441,1
orders,order_status,in,"approved, created, approved, created",8.413,0.054,3829.61,30.33,Seq Scan,Index Scan,99.36,7,99441,1
products,product_category_name,in,"cds_dvds_musicais, seguros_e_servicos",2.086,0.048,964.89,27.26,Seq Scan,Bitmap Heap Scan,97.7,3,32951,1
products,product_category_name,in,"cds_dvds_musicais, seguros_e_servicos, pc_gamer",3.594,0.038,1006.08,31.56,Seq Scan,Bitmap Heap Scan,98.94,6,32951,1
products,product_category_name,in,"telefonia, relogios_presentes",3.483,0.966,964.89,619.6,Seq Scan,Bitmap Heap Scan,72.27,2463,32951,1
products,product_category_name,in,"telefonia, relogios_presentes, brinquedos",4.33,1.071,1006.08,661.4,Seq Scan,Bitmap Heap Scan,75.27,3874,32951,1
products,product_category_name,in,"cds_dvds_musicais, seguros_e_servicos, telefonia, relogios_presentes",4.463,0.827,1047.26,626.02,Seq Scan,Bitmap Heap Scan,81.47,2466,32951,1
orders,customer_id,not_null,IS NOT NULL,11.656,7.384,3332.41,3332.41,Seq Scan,Seq Scan,36.65,99441,99441,1
orders,order_status,not_null,IS NOT NULL,8.813,15.037,3332.41,3332.41,Seq Scan,Seq Scan,-70.62,99441,99441,0
order_items,product_id,not_null,IS NOT NULL,16.432,10.93,3630.5,3630.5,Seq Scan,Seq Scan,33.48,112650,112650,1
order_items,seller_id,not_null,IS NOT NULL,6.499,15.992,3630.5,3630.5,Seq Scan,Seq Scan,-146.07,112650,112650,0
customers,customer_state,not_null,IS NOT NULL,15.825,10.845,2545.41,2545.41,Seq Scan,Seq Scan,31.47,99441,99441,1
sellers,seller_state,not_null,IS NOT NULL,0.322,0.324,66.95,66.95,Seq Scan,Seq Scan,-0.62,3095,3095,0
products,product_category_name,not_null,IS NOT NULL,2.364,3.491,882.51,882.51,Seq Scan,Seq Scan,-47.67,32341,32951,0
