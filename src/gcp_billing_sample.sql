create table sample_data.gcp_billing_sample as
SELECT start_time,end_time,product,cost,usage.amount,usage.unit
FROM `data-analytics-pocs`.public.gcp_billing_export_EXAMPL_E0XD3A_DB33F1;