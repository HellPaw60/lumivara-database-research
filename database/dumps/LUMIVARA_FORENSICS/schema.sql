CREATE TABLE _prov (tbl TEXT, source TEXT);

CREATE TABLE CLASSES (class_id, name, unlock_jobs, unlock_silver, confidence);

CREATE TABLE SKILLS (skill_id, name, class_id, job_level, sp_cost, cooldown_ms, range_px, target, effect, power, multiplier, is_passive, cd_from_aspd, buff_id, confidence);

CREATE TABLE ITEMS (item_id, name, category, kind, weight, sell_price, buy_price, description, confidence);

CREATE TABLE CARDS (card_id, name, bonuses_json, price, description, confidence);

CREATE TABLE STATUSES (status_id, name, kind, icon, duration_ms, params_json, confidence);

CREATE TABLE MAPS (map_id, name, subtitle, width, height, spawn_json, portals_json, confidence);

CREATE TABLE MONSTER_STATUS_ATTACKS (monster_name, status_id, chance, confidence);

CREATE TABLE DROP_RATES (category, rate, confidence);

CREATE TABLE MONSTERS (monster_key, name, level, max_hp, elite, areas_json, base_exp, job_exp, guild_exp, drops_json, exp_samples, confidence);

CREATE TABLE TRANSLATIONS (thai, english);

CREATE TABLE CLIENT_MINING (domain TEXT, finding_json TEXT, source TEXT);

