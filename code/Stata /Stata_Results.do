

//summary statistics
estpost summ CVEvaluation Competent Confident Independent Competitive Intelligent CommunicationSkill InterpersonalSkill LeadershipSkill PersuadingSkill NegotiatingSkill CandidateMale Backoffice Client General Attractive Age EvaluatorMale Married Han birthsouth livesouth University if AI==0

esttab using "XXX", cells("count mean sd min max") nomtitle nonumber noobs replace collabels("Obs" "Mean" "Std. Dev." "Min" "Max") varlabels(_cons "")

estpost summ CVEvaluation Competent Confident Independent Competitive Intelligent CommunicationSkill InterpersonalSkill LeadershipSkill PersuadingSkill NegotiatingSkill CandidateMale Backoffice Client General Attractive if AI==1

esttab using "XXX", cells("count mean sd min max") nomtitle nonumber noobs replace collabels("Obs" "Mean" "Std. Dev." "Min" "Max") varlabels(_cons "")

// VWLS formal:
*vwls1:
reg CVEvaluation Attractive CandidateMale if AI==0

scalar sd0 = e(rmse)

reg CVEvaluation Attractive CandidateMale if AI==1

scalar sd1 = e(rmse)

gen sd_CV1 = sd0 if AI==0
replace sd_CV1 = sd1 if AI==1

vwls CVEvaluation Attractive CandidateMale AI, sd(sd_CV1)

estimates store modelvwls1

*vwls2:
reg CVEvaluation Attractive CandidateMale Attractive_CandidateMale if AI==0

scalar sd20 = e(rmse)

reg CVEvaluation Attractive CandidateMale Attractive_CandidateMale if AI==1

scalar sd21 = e(rmse)

gen sd_CV2 = sd20 if AI==0
replace sd_CV2 = sd21 if AI==1

vwls CVEvaluation Attractive CandidateMale AI Attractive_AI Attractive_CandidateMale AI_CandidateMale, sd(sd_CV2)

estimates store modelvwls2

*vwls3:
vwls CVEvaluation Attractive CandidateMale AI Attractive_AI Attractive_CandidateMale AI_CandidateMale Attractive_AI_CandidateMale, sd(sd_CV2)

estimates store modelvwls3

*vwls4:
reg CVEvaluation Attractive CandidateMale Attractive_CandidateMale if AI==0 & Backoffice==0 & Client==0

scalar sd40 = e(rmse)

reg CVEvaluation Attractive CandidateMale Attractive_CandidateMale if AI==1 & Backoffice==0 & Client==0

scalar sd41 = e(rmse)

gen sd_CV4 = sd40 if AI==0
replace sd_CV4 = sd41 if AI==1

vwls CVEvaluation Attractive CandidateMale AI Attractive_AI Attractive_CandidateMale AI_CandidateMale Attractive_AI_CandidateMale if Backoffice==0 & Client==0, sd(sd_CV4)

estimates store modelvwls4

*vwls5:
reg CVEvaluation Attractive CandidateMale Attractive_CandidateMale if AI==0 & Backoffice==1

scalar sd50 = e(rmse)

reg CVEvaluation Attractive CandidateMale Attractive_CandidateMale if AI==1 & Backoffice==1

scalar sd51 = e(rmse)

gen sd_CV5 = sd50 if AI==0
replace sd_CV5 = sd51 if AI==1

vwls CVEvaluation Attractive CandidateMale AI Attractive_AI Attractive_CandidateMale AI_CandidateMale Attractive_AI_CandidateMale if Backoffice==1, sd(sd_CV5)

estimates store modelvwls5

*vwls6:
reg CVEvaluation Attractive CandidateMale Attractive_CandidateMale if AI==0 & Client==1

scalar sd60 = e(rmse)

reg CVEvaluation Attractive CandidateMale Attractive_CandidateMale if AI==1 & Client==1

scalar sd61 = e(rmse)

gen sd_CV6 = sd60 if AI==0
replace sd_CV6 = sd61 if AI==1

vwls CVEvaluation Attractive CandidateMale AI Attractive_AI Attractive_CandidateMale AI_CandidateMale Attractive_AI_CandidateMale if Client==1, sd(sd_CV6)

estimates store modelvwls6

esttab modelvwls1 modelvwls2 modelvwls3 modelvwls4 modelvwls5 modelvwls6 using "XXX", b(3) p(3) star(* 0.10 ** 0.05 *** 0.01) stats(N r2_a, fmt(0 3)) replace

*vwls7:
reg CVEvaluation Competence SocialSkill if AI==0 

scalar sd70 = e(rmse)

reg CVEvaluation Competence SocialSkill if AI==1

scalar sd71 = e(rmse)

gen sd_CV7 = sd70 if AI==0
replace sd_CV7 = sd71 if AI==1

vwls CVEvaluation Competence SocialSkill AI, sd(sd_CV7)

estimates store modelvwls7

*vwls8:
vwls CVEvaluation Competence SocialSkill AI AI_Competence AI_SocialSkill, sd(sd_CV7)

estimates store modelvwls8

*vwls9:
reg CVEvaluation Competent Confident Independent Competitive Intelligent CommunicationSkill InterpersonalSkill LeadershipSkill PersuadingSkill NegotiatingSkill if AI==0 

scalar sd90 = e(rmse)

reg CVEvaluation Competent Confident Independent Competitive Intelligent CommunicationSkill InterpersonalSkill LeadershipSkill PersuadingSkill NegotiatingSkill if AI==1

scalar sd91 = e(rmse)

gen sd_CV9 = sd90 if AI==0
replace sd_CV9 = sd91 if AI==1

vwls CVEvaluation Competent Confident Independent Competitive Intelligent CommunicationSkill InterpersonalSkill LeadershipSkill PersuadingSkill NegotiatingSkill AI, sd(sd_CV9)

estimates store modelvwls9

*vwls10:
vwls CVEvaluation Competent Confident Independent Competitive Intelligent CommunicationSkill InterpersonalSkill LeadershipSkill PersuadingSkill NegotiatingSkill AI AI_Competent AI_Confident AI_Independent AI_Competitive AI_Intelligent AI_CommunicationSkill AI_InterpersonalSkill AI_LeadershipSkill AI_PersuadingSkill AI_NegotiatingSkill, sd(sd_CV9)

estimates store modelvwls10

esttab modelvwls7 modelvwls8 modelvwls9 modelvwls10 using "XXX", b(3) p(3) star(* 0.10 ** 0.05 *** 0.01) stats(N r2_a, fmt(0 3)) replace

*vwls13:
reg Competent Attractive if AI==0 

scalar sd130 = e(rmse)

reg Competent Attractive if AI==1

scalar sd131 = e(rmse)

gen sd_CV13 = sd130 if AI==0
replace sd_CV13 = sd131 if AI==1

vwls Competent Attractive AI Attractive_AI, sd(sd_CV13)

estimates store modelvwls13

*vwls14:
reg Confident Attractive if AI==0 

scalar sd140 = e(rmse)

reg Confident Attractive if AI==1

scalar sd141 = e(rmse)

gen sd_CV14 = sd140 if AI==0
replace sd_CV14 = sd141 if AI==1

vwls Confident Attractive AI Attractive_AI, sd(sd_CV14)

estimates store modelvwls14

*vwls15:
reg Independent Attractive if AI==0 

scalar sd150 = e(rmse)

reg Independent Attractive if AI==1

scalar sd151 = e(rmse)

gen sd_CV15 = sd150 if AI==0
replace sd_CV15 = sd151 if AI==1

vwls Independent Attractive AI Attractive_AI, sd(sd_CV15)

estimates store modelvwls15

*vwls16:
reg Competitive Attractive if AI==0 

scalar sd160 = e(rmse)

reg Competitive Attractive if AI==1

scalar sd161 = e(rmse)

gen sd_CV16 = sd160 if AI==0
replace sd_CV16 = sd161 if AI==1

vwls Competitive Attractive AI Attractive_AI, sd(sd_CV16)

estimates store modelvwls16

*vwls17:
reg Intelligent Attractive if AI==0 

scalar sd170 = e(rmse)

reg Intelligent Attractive if AI==1

scalar sd171 = e(rmse)

gen sd_CV17 = sd170 if AI==0
replace sd_CV17 = sd171 if AI==1

vwls Intelligent Attractive AI Attractive_AI, sd(sd_CV17)

estimates store modelvwls17

esttab modelvwls13 modelvwls14 modelvwls15 modelvwls16 modelvwls17 using "XXX", b(3) p(3) star(* 0.10 ** 0.05 *** 0.01) stats(N r2_a, fmt(0 3)) replace

*vwls18:
reg CommunicationSkill Attractive if AI==0 

scalar sd180 = e(rmse)

reg CommunicationSkill Attractive if AI==1

scalar sd181 = e(rmse)

gen sd_CV18 = sd180 if AI==0
replace sd_CV18 = sd181 if AI==1

vwls CommunicationSkill Attractive AI Attractive_AI, sd(sd_CV18)

estimates store modelvwls18

*vwls19:
reg InterpersonalSkill Attractive if AI==0 

scalar sd190 = e(rmse)

reg InterpersonalSkill Attractive if AI==1

scalar sd191 = e(rmse)

gen sd_CV19 = sd190 if AI==0
replace sd_CV19 = sd191 if AI==1

vwls InterpersonalSkill Attractive AI Attractive_AI, sd(sd_CV19)

estimates store modelvwls19

*vwls20:
reg LeadershipSkill Attractive if AI==0 

scalar sd200 = e(rmse)

reg LeadershipSkill Attractive if AI==1

scalar sd201 = e(rmse)

gen sd_CV20 = sd200 if AI==0
replace sd_CV20 = sd201 if AI==1

vwls LeadershipSkill Attractive AI Attractive_AI, sd(sd_CV20)

estimates store modelvwls20

*vwls21:
reg PersuadingSkill Attractive if AI==0 

scalar sd210 = e(rmse)

reg PersuadingSkill Attractive if AI==1

scalar sd211 = e(rmse)

gen sd_CV21 = sd210 if AI==0
replace sd_CV21 = sd211 if AI==1

vwls PersuadingSkill Attractive AI Attractive_AI, sd(sd_CV21)

estimates store modelvwls21

*vwls22:
reg NegotiatingSkill Attractive if AI==0 

scalar sd220 = e(rmse)

reg NegotiatingSkill Attractive if AI==1

scalar sd221 = e(rmse)

gen sd_CV22 = sd220 if AI==0
replace sd_CV22 = sd221 if AI==1

vwls NegotiatingSkill Attractive AI Attractive_AI, sd(sd_CV22)

estimates store modelvwls22

esttab modelvwls18 modelvwls19 modelvwls20 modelvwls21 modelvwls22 using "XXX", b(3) p(3) star(* 0.10 ** 0.05 *** 0.01) stats(N r2_a, fmt(0 3)) replace


local southlist  "上海 江苏 浙江 安徽 福建 江西 湖北 湖南 重庆 四川 贵州 云南 广东 广西 海南"

gen birthsouth = 0

foreach p of local southlist {
    replace birthsouth = 1 if strpos(Birth, "`p'") > 0
}

gen livesouth = 0


foreach p of local southlist {
    replace livesouth = 1 if strpos(Lived, "`p'") > 0
}



// Evaluator Gender Effect:
reg CVEvaluation Attractive CandidateMale EvaluatorMale Age Married Han birthsouth livesouth University if AI==0

estimates store model1

reg CVEvaluation Attractive CandidateMale EvaluatorMale Age Married Han birthsouth livesouth University Attractive_EvaluatorMale EvaluatorMale_CandidateMale Attractive_CandidateMale Attract_EvaMale_CandMale if AI==0

estimates store model2

* Evaluator Gender Effect by job feature:
reg CVEvaluation Attractive CandidateMale EvaluatorMale Age Married Han birthsouth livesouth University Attractive_EvaluatorMale EvaluatorMale_CandidateMale Attractive_CandidateMale Attract_EvaMale_CandMale if AI==0 & Backoffice==0 & Client==0

estimates store model3

reg CVEvaluation Attractive CandidateMale EvaluatorMale Age Married Han birthsouth livesouth University Attractive_EvaluatorMale EvaluatorMale_CandidateMale Attractive_CandidateMale Attract_EvaMale_CandMale if AI==0 & Backoffice==1

estimates store model4

reg CVEvaluation Attractive CandidateMale EvaluatorMale Age Married Han birthsouth livesouth University Attractive_EvaluatorMale EvaluatorMale_CandidateMale Attractive_CandidateMale Attract_EvaMale_CandMale if AI==0 & Client==1  

estimates store model5

esttab model1 model2 model3 model4 model5 using "XXX", b(3) p(3) star(* 0.10 ** 0.05 *** 0.01) stats(N r2_a, fmt(0 3)) replace



