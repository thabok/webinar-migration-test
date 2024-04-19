/*
 * Third Party Support License -- for use only to support products
 * interfaced to MathWorks software under terms specified in your
 * company's restricted use license agreement.
 *
 * File: seat_heating_control.c
 *
 * Code generated for Simulink model 'seat_heating_control'.
 *
 * Model version                  : 1.1
 * Simulink Coder version         : 23.2 (R2023b) 01-Aug-2023
 * C/C++ source code generated on : Thu Apr 18 12:38:06 2024
 *
 * Target selection: autosar.tlc
 * Embedded hardware selection: Intel->x86-64 (Windows64)
 * Code generation objectives: Unspecified
 * Validation result: Not run
 */

#include "seat_heating_control.h"
#include "Rte_Type.h"
#include "Platform_Types.h"
#include "zero_crossing_types.h"

/* PublicStructure Variables for Internal Data */
ARID_DEF_seat_heating_control_T seat_heating_control_ARID_DEF;/* '<S5>/Unit Delay2' */

/* Model step function for TID1 */
void runa2(void)                       /* Explicit Task: runa2 */
{
  IDT_ButtonStatus rtb_HeatingRequest_GetButtonPre;

  /* RootInportFunctionCallGenerator generated from: '<Root>/runa2' incorporates:
   *  SubSystem: '<Root>/runa2_sys'
   */
  /* FunctionCaller: '<S3>/HeatingRequest_GetButtonPressed' */
  Rte_Call_HeatingRequest_GetButtonPressed(&rtb_HeatingRequest_GetButtonPre);

  /* Outputs for Triggered SubSystem: '<S3>/convert_to_stage' incorporates:
   *  TriggerPort: '<S5>/Trigger'
   */
  if (rtb_HeatingRequest_GetButtonPre &&
      (seat_heating_control_ARID_DEF.convert_to_stage_Trig_ZCE != POS_ZCSIG)) {
    /* Switch: '<S5>/Switch' incorporates:
     *  Constant: '<S5>/Constant'
     *  Constant: '<S5>/Constant1'
     *  Constant: '<S5>/Constant2'
     *  RelationalOperator: '<S5>/Relational Operator'
     *  Sum: '<S5>/Sum'
     *  UnitDelay: '<S5>/Unit Delay2'
     */
    if ((uint8)(seat_heating_control_ARID_DEF.UnitDelay2_DSTATE + 1U) == 0) {
      seat_heating_control_ARID_DEF.UnitDelay2_DSTATE = 4U;
    } else {
      seat_heating_control_ARID_DEF.UnitDelay2_DSTATE++;
    }

    /* End of Switch: '<S5>/Switch' */
  }

  seat_heating_control_ARID_DEF.convert_to_stage_Trig_ZCE =
    rtb_HeatingRequest_GetButtonPre;

  /* End of Outputs for SubSystem: '<S3>/convert_to_stage' */
  /* End of Outputs for RootInportFunctionCallGenerator generated from: '<Root>/runa2' */

  /* RootInportFunctionCallGenerator generated from: '<Root>/runa2' incorporates:
   *  SubSystem: '<Root>/runa2_sys'
   */
  /* DataTransferBlock generated from: '<Root>/runa2_sys' incorporates:
   *  SignalConversion generated from: '<S3>/TemperatureStage_write'
   *  UnitDelay: '<S5>/Unit Delay2'
   */
  Rte_IrvIWrite_runa2_TemperatureStage
    (seat_heating_control_ARID_DEF.UnitDelay2_DSTATE);

  /* End of Outputs for RootInportFunctionCallGenerator generated from: '<Root>/runa2' */
}

/* Model step function for TID2 */
void runa1(void)                       /* Explicit Task: runa1 */
{
  /* RootInportFunctionCallGenerator generated from: '<Root>/runa1' incorporates:
   *  SubSystem: '<Root>/runa1_sys'
   */
  /* Logic: '<S2>/Logical Operator' incorporates:
   *  Constant: '<S2>/Constant1'
   *  Inport: '<Root>/PowerMgtState_PowerMgtState'
   *  Inport: '<Root>/PowerMgtState_PowerMgtState_ErrorStatus'
   *  Inport: '<Root>/SeatOccupied_SeatOccupied'
   *  RelationalOperator: '<S2>/Relational Operator'
   *  RelationalOperator: '<S2>/Relational Operator1'
   *  RelationalOperator: '<S2>/Relational Operator2'
   */
  seat_heating_control_ARID_DEF.LogicalOperator_c =
    (Rte_IStatus_runa1_PowerMgtState_PowerMgtState() == 0);
  seat_heating_control_ARID_DEF.LogicalOperator_c =
    (Rte_IRead_runa1_SeatOccupied_SeatOccupied() &&
     (Rte_IRead_runa1_PowerMgtState_PowerMgtState() == OK) &&
     seat_heating_control_ARID_DEF.LogicalOperator_c);

  /* End of Outputs for RootInportFunctionCallGenerator generated from: '<Root>/runa1' */

  /* DataTransferBlock generated from: '<Root>/runa1_sys' */
  Rte_IrvIWrite_runa1_ActivationCondition
    (seat_heating_control_ARID_DEF.LogicalOperator_c);
}

/* Model step function for TID3 */
void runa3(void)                       /* Explicit Task: runa3 */
{
  IDT_Temperature rtb_MultiportSwitch;
  uint8 TemperatureStage;
  boolean tmp[3];
  boolean rtb_RelationalOperator2_h;

  /* DataTransferBlock generated from: '<Root>/runa2_sys' */
  TemperatureStage = Rte_IrvIRead_runa3_TemperatureStage();

  /* RootInportFunctionCallGenerator generated from: '<Root>/runa3' incorporates:
   *  SubSystem: '<Root>/runa3_sys'
   */
  /* Outputs for Enabled SubSystem: '<S4>/Subsystem' incorporates:
   *  EnablePort: '<S6>/Enable'
   */
  /* DataTransferBlock generated from: '<Root>/runa1_sys' */
  if (Rte_IrvIRead_runa3_ActivationCondition()) {
    /* MultiPortSwitch: '<S6>/Multiport Switch' */
    switch (TemperatureStage) {
     case 1:
      /* MultiPortSwitch: '<S6>/Multiport Switch' incorporates:
       *  Constant: '<S6>/CPA_TemperatureRanges_TemperatureRanges'
       */
      rtb_MultiportSwitch = Rte_Prm_TemperatureRanges_TemperatureStage1();
      break;

     case 2:
      /* MultiPortSwitch: '<S6>/Multiport Switch' incorporates:
       *  Constant: '<S6>/CPA_TemperatureRanges_TemperatureStage2'
       */
      rtb_MultiportSwitch = Rte_Prm_TemperatureRanges_TemperatureStage2();
      break;

     case 3:
      /* MultiPortSwitch: '<S6>/Multiport Switch' incorporates:
       *  Constant: '<S6>/CPA_TemperatureRanges_TemperatureStage3'
       */
      rtb_MultiportSwitch = Rte_Prm_TemperatureRanges_TemperatureStage3();
      break;

     default:
      /* MultiPortSwitch: '<S6>/Multiport Switch' incorporates:
       *  Constant: '<S6>/Constant1'
       */
      rtb_MultiportSwitch = 0U;
      break;
    }

    /* End of MultiPortSwitch: '<S6>/Multiport Switch' */

    /* FunctionCaller: '<S6>/HeatingActivate_SetHeatingCoil' */
    Rte_Call_HeatingActivate_SetHeatingCoil(rtb_MultiportSwitch);

    /* RelationalOperator: '<S6>/Relational Operator2' incorporates:
     *  Constant: '<S6>/Constant3'
     */
    rtb_RelationalOperator2_h = (TemperatureStage == 2);

    /* RelationalOperator: '<S6>/Relational Operator3' incorporates:
     *  Constant: '<S6>/Constant4'
     */
    seat_heating_control_ARID_DEF.RelationalOperator3 = (TemperatureStage == 3);

    /* Logic: '<S6>/Logical Operator' incorporates:
     *  Constant: '<S6>/Constant2'
     *  RelationalOperator: '<S6>/Relational Operator1'
     */
    seat_heating_control_ARID_DEF.LogicalOperator = ((TemperatureStage == 1) ||
      rtb_RelationalOperator2_h ||
      seat_heating_control_ARID_DEF.RelationalOperator3);

    /* Logic: '<S6>/Logical Operator1' */
    seat_heating_control_ARID_DEF.LogicalOperator1 = (rtb_RelationalOperator2_h ||
      seat_heating_control_ARID_DEF.RelationalOperator3);
  }

  /* End of DataTransferBlock generated from: '<Root>/runa1_sys' */
  /* End of Outputs for SubSystem: '<S4>/Subsystem' */
  /* End of Outputs for RootInportFunctionCallGenerator generated from: '<Root>/runa3' */

  /* Outport: '<Root>/LEDFeedback_LEDFeedback' */
  tmp[0] = seat_heating_control_ARID_DEF.LogicalOperator;
  tmp[1] = seat_heating_control_ARID_DEF.LogicalOperator1;
  tmp[2] = seat_heating_control_ARID_DEF.RelationalOperator3;
  Rte_IWrite_runa3_LEDFeedback_LEDFeedback(tmp);
}

/* Model initialize function */
void SeatHeatControl_Init(void)
{
  {
    boolean tmpIWrite[3];
    seat_heating_control_ARID_DEF.convert_to_stage_Trig_ZCE = POS_ZCSIG;

    /* SystemInitialize for Outport: '<Root>/LEDFeedback_LEDFeedback' incorporates:
     *  Logic: '<S6>/Logical Operator'
     *  Logic: '<S6>/Logical Operator1'
     *  RelationalOperator: '<S6>/Relational Operator3'
     */
    tmpIWrite[0] = seat_heating_control_ARID_DEF.LogicalOperator;
    tmpIWrite[1] = seat_heating_control_ARID_DEF.LogicalOperator1;
    tmpIWrite[2] = seat_heating_control_ARID_DEF.RelationalOperator3;

    /* Outport: '<Root>/LEDFeedback_LEDFeedback' */
    Rte_IWrite_SeatHeatControl_Init_LEDFeedback_LEDFeedback(tmpIWrite);
  }
}

/*
 * File trailer for generated code.
 *
 * [EOF]
 */
