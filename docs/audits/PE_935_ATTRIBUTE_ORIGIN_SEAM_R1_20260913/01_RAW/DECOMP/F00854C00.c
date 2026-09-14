
int __thiscall FUN_00854c00(int param_1,_Slist_node_base *param_2)

{
  vector<struct_stlp_std::priv::_Slist_node_base*,class_stlp_std::allocator<struct_stlp_std::priv::_Slist_node_base*>_>
  *this;
  uint uVar1;
  allocator<struct_stlp_std::priv::_Slist_node_base*> local_11;
  int local_10;
  void *local_c;
  undefined *puStack_8;
  undefined4 local_4;
  
  puStack_8 = &LAB_00a292b0;
  local_c = ExceptionList;
  ExceptionList = &local_c;
  *(undefined4 *)(param_1 + 4) = 0;
  this = (vector<struct_stlp_std::priv::_Slist_node_base*,class_stlp_std::allocator<struct_stlp_std::priv::_Slist_node_base*>_>
          *)(param_1 + 8);
  local_4 = 1;
  local_10 = param_1;
  stlp_std::
  vector<struct_stlp_std::priv::_Slist_node_base*,class_stlp_std::allocator<struct_stlp_std::priv::_Slist_node_base*>_>
  ::
  vector<struct_stlp_std::priv::_Slist_node_base*,class_stlp_std::allocator<struct_stlp_std::priv::_Slist_node_base*>_>
            (this,&local_11);
  *(undefined4 *)(param_1 + 0x18) = 0x3f800000;
  local_4 = CONCAT31(local_4._1_3_,3);
  *(undefined4 *)(param_1 + 0x14) = 0;
  uVar1 = stlp_std::priv::_Stl_prime<bool>::_S_next_size((uint)param_2);
  stlp_std::
  vector<struct_stlp_std::priv::_Slist_node_base*,class_stlp_std::allocator<struct_stlp_std::priv::_Slist_node_base*>_>
  ::reserve(this,uVar1 + 1);
  param_2 = (_Slist_node_base *)0x0;
  stlp_std::
  vector<struct_stlp_std::priv::_Slist_node_base*,class_stlp_std::allocator<struct_stlp_std::priv::_Slist_node_base*>_>
  ::_M_fill_assign(this,uVar1 + 1,&param_2);
  ExceptionList = local_c;
  return param_1;
}

