create or replace table sample_data.gcp_billing_sample as
SELECT EXTRACT(DATE FROM start_time) start_time,
EXTRACT(DATE FROM end_time) end_time,
resource_type,
product,
cost,
usage.amount,
usage.unit
FROM `data-analytics-pocs`.public.gcp_billing_export_EXAMPL_E0XD3A_DB33F1;

create or replace table sample_data.daily_data as
select
    start_time,
    product,unit,
    resource_type,
    sum(cost) cost ,
    sum(amount) usage_amount
from sample_data.gcp_billing_sample
group by 1,2,3,4;

select * from (
select product, unit, resource_type, sum(cost) cost, sum(usage_amount),count(*) cnt
from sample_data.daily_data
where product in ("BigQuery","Cloud Storage", "Compute Engine")
group by 1,2, 3 order by 1,3 ) where cost > 1

create table sample_data.top_3_prods as
with top3 as
(select * from (
select product, unit, resource_type, sum(cost) cost, sum(usage_amount),count(*) cnt
from sample_data.daily_data
where product in ("BigQuery","Cloud Storage", "Compute Engine")
group by 1,2, 3 order by 1,3 ) where cost > 1)
select t1.*
from `intense-arbor-186802.sample_data.daily_data` t1 inner join top3 t2
on t1.product = t2.product
and t1.unit = t2.unit
and t1.resource_type = t2.resource_type
