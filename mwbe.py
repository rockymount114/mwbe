QUERY_TXT = '''SELECT 

dept.glsg_code			AS department_no
, dept.glsg_shdesc		AS dept_desc
, div.glsg_code			AS division_no
, div.glsg_desc			AS divsion_desc
, dd.*


FROM (

SELECT
    h.apih_vendor AS 'VendorNumber',
	apvn_genl_type,

    --CASE
    --    WHEN d.a_object IN ('112500', '192001', '275000', '275100', '386013', '389029', '392000', '476000', '476001', '476002', '476003', '476004', '476005', '476006', '476007', '476008', '476009', '476010', '476011', '476011', '476012', '476013', '476013', '476014', '476015', '476016', '476017', '476018', '476018', '476019', '476020', '476021', '476022') THEN 1
    --    WHEN d.a_object IN ('496100', '496111', '496112', '496113', '496114', '496115', '496123', '496160', '496161', '496162', '496163', '496164') THEN 1
    --    WHEN d.a_object IN ('449100', '449105', '449106') THEN 1
    --    WHEN d.a_object IN ('444000') THEN 2  -- need purchasing to check
    --    WHEN d.a_object IN ('557000', '419200', '431200', '419000', '419100', '439607', '463006', '441100', '469034', '469055', '432100', '439900', '418600', '445000', '449000', '496111', '496099') THEN 1
    --    ELSE 0
    --END AS flag,

    d.a_org,
    d.a_object,

	LEFT(d.a_org, 3)			AS Fund,
	SUBSTRING(d.a_org, 4, 2)	AS Dept,
	RIGHT(d.a_org, 3)			AS Division,

 --   v.apvn_mbe_wbe				AS 'isMWBE',
	--CASE WHEN v.apvn_genl_type IN ('MBE', 'WBE') OR v.apvn_mbe_wbe = 'Y' THEN 1 ELSE 0 END		MWBE_TYPE,

	CASE WHEN v.apvn_mbe_wbe = 'Y' OR (v.apvn_genl_type IN ('MBE', 'WBE')) THEN 1 ELSE 0 END	mwbe_status
	,

    d.a_line_item_amount AS 'LineCost',
    d.a_invoice_number AS 'InvoiceNumber',
	d.a_invoice_number AS 'Doc_Number',

    h.apih_inv_total,
    h.apih_inv_net,
    h.apih_desc,
    --m.glma_desc,
    --m.glma_short_desc,
    apih_je_year,
    apih_je_per,
    h.apih_check_no,
    h.apih_inv_num,
    
    h.apih_doc,
    h.apih_gl_effec_date,
    h.apih_check_date,
    h.apih_inv_date,
    h.apih_alpha_sort						AS 'Vendor_name',
    h.apih_county_cd,
    h.apih_po_fsc_yr,
    h.apih_type,
    h.apih_voucher,
    h.apih_warrant,
    h.apih_po

    --h.apih_dept  -- division no

    --m.glma_seg1,
    --m.glma_seg3
FROM dbo.apinvoih AS h

JOIN dbo.apvendor AS v 
ON h.apih_vendor = v.apvn_vend

LEFT JOIN dbo.ap_invoice AS d 
ON h.apih_doc = d.a_invoice_number
AND h.apih_vendor = a_vendor_number

LEFT JOIN (
    SELECT
        DISTINCT
        m.glma_org,
        m.glma_obj,
		--m.glma_project,
        --m.glma_desc,
        --m.glma_short_desc,
        m.glma_seg1,
        m.glma_seg3
    FROM dbo.glmaster AS m

    WHERE 
	
	LEN(glma_org) = 8
        AND glma_org > '110'
        AND glma_stat = 'A'

) AS m ON d.a_org = m.glma_org AND d.a_object = m.glma_obj


WHERE
    --v.apvn_stat_cd = 'A'
    --AND 
	v.apvn_genl_type NOT IN ('EMP', 'RFD')

    AND LEN(d.a_org) >= 8
    AND d.a_org > '110'
    AND h.apih_inv_total >= 0
    AND h.apih_gl_effec_date >= '2020-07-01'



) dd

LEFT JOIN (

		SELECT * FROM dbo.glsegmnt
		WHERE glsg_type = 2  -- Department code
		) AS dept
		ON dept.glsg_code = dd.Dept

LEFT JOIN (

		SELECT * FROM dbo.glsegmnt
		WHERE glsg_type = 3  -- division code
		) AS div
		ON div.glsg_code = dd.Division

--WHERE 

--(d.MWBE_TYPE = 1 OR d.isMWBE = 'Y')
--and 
--dd.apih_je_year = 2023
-- and dd.mwbe_status = 1

'''