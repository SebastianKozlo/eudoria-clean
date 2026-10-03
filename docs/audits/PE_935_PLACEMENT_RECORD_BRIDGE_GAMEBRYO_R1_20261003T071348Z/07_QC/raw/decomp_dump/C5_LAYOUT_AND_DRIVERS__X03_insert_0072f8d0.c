// source: C5_LAYOUT_AND_DRIVERS.json :: X03_insert_0072f8d0

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 * __thiscall
FUN_0072f8d0(_Rb_tree_node_base *param_1_00,undefined4 *param_1,uint *param_2)

{
  _Rb_tree_node_base *p_Var1;
  _Rb_tree_node_base *p_Var2;
  _Rb_tree_node_base *p_Var3;
  bool bVar4;
  
  p_Var1 = *(_Rb_tree_node_base **)(param_1_00 + 4);
  bVar4 = true;
  p_Var3 = param_1_00;
  if (p_Var1 != (_Rb_tree_node_base *)0x0) {
    do {
      p_Var3 = p_Var1;
      bVar4 = *param_2 < *(uint *)(p_Var3 + 0x10);
      if (bVar4) {
        p_Var1 = *(_Rb_tree_node_base **)(p_Var3 + 8);
      }
      else {
        p_Var1 = *(_Rb_tree_node_base **)(p_Var3 + 0xc);
      }
    } while (p_Var1 != (_Rb_tree_node_base *)0x0);
  }
  p_Var2 = p_Var3;
  if (bVar4) {
    if (p_Var3 == *(_Rb_tree_node_base **)(param_1_00 + 8)) {
      if (p_Var3 == param_1_00) {
        p_Var1 = (_Rb_tree_node_base *)FUN_0072f7f0(param_2);
        *(_Rb_tree_node_base **)(p_Var3 + 8) = p_Var1;
        *(_Rb_tree_node_base **)(param_1_00 + 4) = p_Var1;
        *(_Rb_tree_node_base **)(param_1_00 + 0xc) = p_Var1;
      }
      else if ((p_Var3 == (_Rb_tree_node_base *)0x0) && (_DAT_00000010 <= *param_2)) {
        p_Var1 = (_Rb_tree_node_base *)FUN_0072f7f0(param_2);
        _DAT_0000000c = p_Var1;
        if (*(int *)(param_1_00 + 0xc) == 0) {
          *(_Rb_tree_node_base **)(param_1_00 + 0xc) = p_Var1;
        }
      }
      else {
        p_Var1 = (_Rb_tree_node_base *)FUN_0072f7f0(param_2);
        *(_Rb_tree_node_base **)(p_Var3 + 8) = p_Var1;
        if (p_Var3 == *(_Rb_tree_node_base **)(param_1_00 + 8)) {
          *(_Rb_tree_node_base **)(param_1_00 + 8) = p_Var1;
        }
      }
      *(_Rb_tree_node_base **)(p_Var1 + 4) = p_Var3;
      stlp_std::priv::_Rb_global<bool>::_Rebalance(p_Var1,(_Rb_tree_node_base **)(param_1_00 + 4));
      *(int *)(param_1_00 + 0x10) = *(int *)(param_1_00 + 0x10) + 1;
      *param_1 = p_Var1;
      *(undefined *)(param_1 + 1) = 1;
      return param_1;
    }
    p_Var2 = stlp_std::priv::_Rb_global<bool>::_M_decrement(p_Var3);
  }
  if (*(uint *)(p_Var2 + 0x10) < *param_2) {
    if (p_Var3 == param_1_00) {
      p_Var1 = (_Rb_tree_node_base *)FUN_0072f7f0(param_2);
      *(_Rb_tree_node_base **)(p_Var3 + 8) = p_Var1;
      *(_Rb_tree_node_base **)(param_1_00 + 4) = p_Var1;
      *(_Rb_tree_node_base **)(param_1_00 + 0xc) = p_Var1;
    }
    else if ((p_Var1 == (_Rb_tree_node_base *)0x0) && (*(uint *)(p_Var3 + 0x10) <= *param_2)) {
      p_Var1 = (_Rb_tree_node_base *)FUN_0072f7f0(param_2);
      *(_Rb_tree_node_base **)(p_Var3 + 0xc) = p_Var1;
      if (p_Var3 == *(_Rb_tree_node_base **)(param_1_00 + 0xc)) {
        *(_Rb_tree_node_base **)(param_1_00 + 0xc) = p_Var1;
      }
    }
    else {
      p_Var1 = (_Rb_tree_node_base *)FUN_0072f7f0(param_2);
      *(_Rb_tree_node_base **)(p_Var3 + 8) = p_Var1;
      if (p_Var3 == *(_Rb_tree_node_base **)(param_1_00 + 8)) {
        *(_Rb_tree_node_base **)(param_1_00 + 8) = p_Var1;
      }
    }
    *(_Rb_tree_node_base **)(p_Var1 + 4) = p_Var3;
    stlp_std::priv::_Rb_global<bool>::_Rebalance(p_Var1,(_Rb_tree_node_base **)(param_1_00 + 4));
    *(int *)(param_1_00 + 0x10) = *(int *)(param_1_00 + 0x10) + 1;
    *param_1 = p_Var1;
    *(undefined *)(param_1 + 1) = 1;
    return param_1;
  }
  *param_1 = p_Var2;
  *(undefined *)(param_1 + 1) = 0;
  return param_1;
}

