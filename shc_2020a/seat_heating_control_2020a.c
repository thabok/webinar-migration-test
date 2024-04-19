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
 * Simulink Coder version         : 9.3 (R2020a) 18-Nov-2019
 * C/C++ source code generated on : Thu Apr 18 12:37:40 2024
 *
 * Target selection: autosar.tlc
 * Embedded hardware selection: Intel->x86-64 (Windows64)
 * Code generation objectives: Unspecified
 * Validation result: Not run
 */

#include "seat_heating_control.h"
#include "seat_heating_control_private.h"

/* Block signals (default storage) */
B_seat_heating_control_T seat_heating_control_B;

/* Block states (default storage) */
DW_seat_heating_control_T seat_heating_control_DW;

/* Previous zero-crossings (trigger) states */
PrevZCX_seat_heating_control_T seat_heating_control_PrevZCX;

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
      (seat_heating_control_PrevZCX.convert_to_stage_Trig_ZCE != POS_ZCSIG)) {
    /* Sum: '<S5>/Sum' incorporates:
     *  Constant: '<S5>/Constant'
     *  UnitDelay: '<S5>/Unit Delay2'
     */
    seat_heating_control_DW.UnitDelay2_DSTATE++;

    /* Switch: '<S5>/Switch' incorporates:
     *  Constant: '<S5>/Constant1'
     *  Constant: '<S5>/Constant2'
     *  RelationalOperator: '<S5>/Relational Operator'
     *  UnitDelay: '<S5>/Unit Delay2'
     */
    if (seat_heating_control_DW.UnitDelay2_DSTATE == 0) {
      seat_heating_control_DW.UnitDelay2_DSTATE = 4U;
    }

    /* End of Switch: '<S5>/Switch' */
  }

  seat_heating_control_PrevZCX.convert_to_stage_Trig_ZCE =
    rtb_HeatingRequest_GetButtonPre;

  /* End of Outputs for SubSystem: '<S3>/convert_to_stage' */

  /* SignalConversion generated from: '<S3>/TemperatureStage_write' incorporates:
   *  UnitDelay: '<S5>/Unit Delay2'
   */
  Rte_IrvIWrite_runa2_TemperatureStage(seat_heating_control_DW.UnitDelay2_DSTATE);

  /* End of Outputs for RootInportFunctionCallGenerator generated from: '<Root>/runa2' */
}

/* Model step function for TID2 */
void runa1(void)                       /* Explicit Task: runa1 */
{
  /* RootInportFunctionCallGenerator generated from: '<Root>/runa1' incorporates:
   *  SubSystem: '<Root>/runa1_sys'
   */
  /* SignalConversion generated from: '<S2>/ActivationCondition_write' incorporates:
   *  Constant: '<S2>/Constant1'
   *  Inport: '<Root>/PowerMgtState_PowerMgtState'
   *  Inport: '<Root>/PowerMgtState_PowerMgtState_ErrorStatus'
   *  Inport: '<Root>/SeatOccupied_SeatOccupied'
   *  Logic: '<S2>/Logical Operator'
   *  RelationalOperator: '<S2>/Relational Operator'
   *  RelationalOperator: '<S2>/Relational Operator1'
   *  RelationalOperator: '<S2>/Relational Operator2'
   */
  Rte_IrvIWrite_runa1_ActivationCondition
    (Rte_IRead_runa1_SeatOccupied_SeatOccupied() &&
     (Rte_IRead_runa1_PowerMgtState_PowerMgtState() == OK) &&
     (Rte_IStatus_runa1_PowerMgtState_PowerMgtState() == 0));

  /* End of Outputs for RootInportFunctionCallGenerator generated from: '<Root>/runa1' */
}

/* Model step function for TID3 */
void runa3(void)                       /* Explicit Task: runa3 */
{
  uint8 rtb_TmpSignalConversionAtTemper;
  IDT_Temperature rtb_MultiportSwitch;
  boolean rtb_RelationalOperator2_h;
  boolean tmp[3];

  /* RootInportFunctionCallGenerator generated from: '<Root>/runa3' incorporates:
   *  SubSystem: '<Root>/runa3_sys'
   */
  /* SignalConversion generated from: '<S4>/TemperatureStage_read' incorporates:
   *  SignalConversion generated from: '<S3>/TemperatureStage_write'
   */
  rtb_TmpSignalConversionAtTemper = Rte_IrvIRead_runa3_TemperatureStage();

  /* Outputs for Enabled SubSystem: '<S4>/Subsystem' incorporates:
   *  EnablePort: '<S6>/Enable'
   */
  /* SignalConversion generated from: '<S4>/ActivationCondition_read' incorporates:
   *  SignalConversion generated from: '<S2>/ActivationCondition_write'
   */
  if (Rte_IrvIRead_runa3_ActivationCondition()) {
    /* MultiPortSwitch: '<S6>/Multiport Switch' incorporates:
     *  Constant: '<S6>/CPA_TemperatureRanges_TemperatureRanges'
     *  Constant: '<S6>/CPA_TemperatureRanges_TemperatureStage2'
     *  Constant: '<S6>/CPA_TemperatureRanges_TemperatureStage3'
     *  Constant: '<S6>/Constant1'
     */
    switch (rtb_TmpSignalConversionAtTemper) {
     case 1:
      rtb_MultiportSwitch = Rte_Prm_TemperatureRanges_TemperatureStage1();
      break;

     case 2:
      rtb_MultiportSwitch = Rte_Prm_TemperatureRanges_TemperatureStage2();
      break;

     case 3:
      rtb_MultiportSwitch = Rte_Prm_TemperatureRanges_TemperatureStage3();
      break;

     default:
      rtb_MultiportSwitch = 0U;
      break;
    }

    /* End of MultiPortSwitch: '<S6>/Multiport Switch' */

    /* FunctionCaller: '<S6>/HeatingActivate_SetHeatingCoil' */
    Rte_Call_HeatingActivate_SetHeatingCoil(rtb_MultiportSwitch);

    /* RelationalOperator: '<S6>/Relational Operator2' incorporates:
     *  Constant: '<S6>/Constant3'
     */
    rtb_RelationalOperator2_h = (rtb_TmpSignalConversionAtTemper == 2);

    /* RelationalOperator: '<S6>/Relational Operator3' incorporates:
     *  Constant: '<S6>/Constant4'
     */
    seat_heating_control_B.RelationalOperator3 =
      (rtb_TmpSignalConversionAtTemper == 3);

    /* Logic: '<S6>/Logical Operator' incorporates:
     *  Constant: '<S6>/Constant2'
     *  RelationalOperator: '<S6>/Relational Operator1'
     */
    seat_heating_control_B.LogicalOperator = ((rtb_TmpSignalConversionAtTemper ==
      1) || rtb_RelationalOperator2_h ||
      seat_heating_control_B.RelationalOperator3);

    /* Logic: '<S6>/Logical Operator1' */
    seat_heating_control_B.LogicalOperator1 = (rtb_RelationalOperator2_h ||
      seat_heating_control_B.RelationalOperator3);
  }

  /* End of SignalConversion generated from: '<S4>/ActivationCondition_read' */
  /* End of Outputs for SubSystem: '<S4>/Subsystem' */
  /* End of Outputs for RootInportFunctionCallGenerator generated from: '<Root>/runa3' */

  /* Outport: '<Root>/LEDFeedback_LEDFeedback' */
  tmp[0] = seat_heating_control_B.LogicalOperator;
  tmp[1] = seat_heating_control_B.LogicalOperator1;
  tmp[2] = seat_heating_control_B.RelationalOperator3;
  Rte_IWrite_runa3_LEDFeedback_LEDFeedback(tmp);
}

/* Model initialize function */
void SeatHeatControl_Init(void)
{
  {
    boolean tmpIWrite[3];
    seat_heating_control_PrevZCX.convert_to_stage_Trig_ZCE = POS_ZCSIG;

    /* SystemInitialize for Outport: '<Root>/LEDFeedback_LEDFeedback' */
    tmpIWrite[0] = seat_heating_control_B.LogicalOperator;
    tmpIWrite[1] = seat_heating_control_B.LogicalOperator1;
    tmpIWrite[2] = seat_heating_control_B.RelationalOperator3;

    /* Outport: '<Root>/LEDFeedback_LEDFeedback' */
    Rte_IWrite_SeatHeatControl_Init_LEDFeedback_LEDFeedback(tmpIWrite);
  }
}

/*
 * File trailer for generated code.
 *
 * [EOF]
 */
