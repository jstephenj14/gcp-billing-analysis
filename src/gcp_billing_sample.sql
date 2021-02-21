# select project.id, count(*),sum(cost) cost from `data-analytics-pocs`.public.gcp_billing_export_EXAMPL_E0XD3A_DB33F1 group by 1 order by 2 desc;

# select * from `data-analytics-pocs`.public.gcp_billing_export_EXAMPL_E0XD3A_DB33F1 limit 3;

create or replace table sample_data.gcp_billing_sample as
SELECT EXTRACT(DATE FROM start_time) start_time,
EXTRACT(DATE FROM end_time) end_time,
resource_type,
usage.unit,
product,
project.id as project_id,
l.value as project_tag,
cost,
usage.amount
FROM `data-analytics-pocs`.public.gcp_billing_export_EXAMPL_E0XD3A_DB33F1, UNNEST(labels) as l;

create or replace table sample_data.daily_data as
select
    start_time,
    product,
    unit,
    resource_type,
    # project_id,
    sum(cost) cost ,
    sum(amount) usage_amount
from sample_data.gcp_billing_sample
group by 1,2,3,4;

create or replace table sample_data.top_3_prods as
with top3 as
(select * from (
select product,
unit, resource_type, sum(cost) cost, sum(usage_amount),count(*) cnt
from sample_data.daily_data
where product in ("BigQuery","Cloud Storage", "Compute Engine")
# and project_id = "Galactica"
group by 1,2, 3 order by 1,3 ) where cost > 1)
select t1.*
from `intense-arbor-186802.sample_data.daily_data` t1 inner join top3 t2
on t1.product = t2.product
and t1.unit = t2.unit
and t1.resource_type = t2.resource_type
# where t1.project_id = "Galactica";

-- access struct from bq table
-- https://stackoverflow.com/questions/39109817/cannot-access-field-in-big-query-with-type-arraystructhitnumber-int64-time-in