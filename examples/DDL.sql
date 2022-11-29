create table sisu_facts (
	subgroup_id bigint,
	confidence ENUM('CONFIDENCE_LEVEL_UNKNOWN', 'CONFIDENCE_LEVEL_HIGH', 'CONFIDENCE_LEVEL_MEDIUM', 'CONFIDENCE_LEVEL_LOW'),
	factor_0_dimension text,
	factor_0_value text,
	factor_1_dimension text,
	factor_1_value text,
	factor_2_dimension text,
	factor_2_value text,
	impact numeric,
	previous_period_size numeric,
	recent_period_size numeric,
	previous_period_value numeric,
	recent_period_value numeric,
	previous_period_start timestamp,
	previous_period_end timestamp,
	recent_period_start timestamp,
	recent_period_end timestamp,
	size numeric,
	value numeric,
	group_a_size numeric,
	group_b_size numeric,
	group_a_value numeric,
	group_b_value numeric,
	group_a_name text,
	group_b_name text
);