<template>
  <el-row>
    <el-col :span='24'>
      <el-steps :active="steps" finish-status="wait" align-center class="marginBottom">
        <el-step title="审核计划" @click.native="toStep(0)" class="cursor-pointer"></el-step>
        <el-step title="设备配置" @click.native="toStep(1)" class="cursor-pointer"></el-step>
        <el-step title="执行计划列表" @click.native="toStep(2)" class="cursor-pointer"></el-step>
      </el-steps>
       <el-row v-if='steps==0'>
          <el-col :span='24' class="platformContainer">
           <div style="height:40px;fontSize:16px;fontWeight:700;">批次列表</div>
           <div class="marginBottom"><el-button type="primary" icon="el-icon-folder-checked" size='mini' @click="shMultiplebatch">多批次审核</el-button></div>
              <el-table
                  :data="batchTableData.data"
                  highlight-current-row
                  size='small'
                  border
                  ref="batchmultipleTable"
                  @select='getAllbatchrow'
                  style="width: 100%">
                  <el-table-column type="selection" width="55"></el-table-column>
                  <el-table-column v-for="item in batchtableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
                  <el-table-column prop="PlanStatus" label="计划状态">
                    <template slot-scope="scope">
                      <span class="color-red" v-if="scope.row.PlanStatus === '审核未通过'">{{ scope.row.PlanStatus }}</span>
                      <span class="color-orange" v-if="scope.row.PlanStatus === '待审核'">{{ scope.row.PlanStatus }}</span>
                      <span class="color-purple" v-if="scope.row.PlanStatus === '待配置'">{{ scope.row.PlanStatus }}</span>
                      <span class="color-red" v-if="scope.row.PlanStatus === '撤回'">{{ scope.row.PlanStatus }}</span>
                      <span class="color-lightgreen" v-if="scope.row.PlanStatus === '待下发'">{{ scope.row.PlanStatus }}</span>
                      <span class="color-darkblue" v-if="scope.row.PlanStatus === '已下发'">{{ scope.row.PlanStatus }}</span>
                    </template>
                  </el-table-column>
                  <el-table-column label="操作" fixed="right" width='160'>
                    <template slot-scope="scope">
                      <el-button
                        size="mini"
                        type='success'
                         v-if="scope.row.PlanStatus==='待审核'"
                        @click="checkPass(scope.$index, scope.row)">通过</el-button>
                      <el-button
                        size="mini"
                        type="primary"
                         v-if="scope.row.PlanStatus==='待审核'"
                        @click="checkNopass(scope.$index, scope.row)">不通过</el-button>
                      <el-button
                        size="mini"
                        v-if="scope.row.PlanStatus==='审核未通过'"
                        @click="searchWhyNopass(scope.$index, scope.row)"
                       >未通过原因</el-button>
                    </template>
                  </el-table-column>
              </el-table>
              <div class="paginationClass">
                  <el-pagination background  layout="total,prev, pager, next, jumper"
                  :total="batchTableData.total"
                  :current-page="batchTableData.offset"
                  :page-size="batchTableData.limit"
                  @size-change="batchHandleSizeChange"
                  @current-change="batchHandleCurrentChange">
                  </el-pagination>
            </div>
        </el-col>
       </el-row>
       
       <el-row v-if='steps==1'>
         <div style="margin:20px 0">
          <el-radio-group v-model="radio3" size="small" @change="setStatus">
            <el-radio-button label="待配置"></el-radio-button>
            <el-radio-button label="撤回"></el-radio-button>
          </el-radio-group>
        </div>
          <el-col :span='24' class="platformContainer" v-if="radio3==='待配置'">
           <div style="height:40px;fontSize:16px;fontWeight:700;">待配置列表</div>
              <el-table
                  :data="xfTableData.data"
                  highlight-current-row
                  size='small'
                  border
                  ref="xfmultipleTable"
                  @row-click="xfTabCurrentChange"
                  style="width: 100%">
                  <el-table-column v-for="item in batchtableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
                  <el-table-column prop="PlanStatus" label="计划状态">
                    <template slot-scope="scope">
                      <span class="color-red" v-if="scope.row.PlanStatus === '审核未通过'">{{ scope.row.PlanStatus }}</span>
                      <span class="color-orange" v-if="scope.row.PlanStatus === '待审核'">{{ scope.row.PlanStatus }}</span>
                      <span class="color-purple" v-if="scope.row.PlanStatus === '待配置'">{{ scope.row.PlanStatus }}</span>
                      <span class="color-red" v-if="scope.row.PlanStatus === '撤回'">{{ scope.row.PlanStatus }}</span>
                      <span class="color-lightgreen" v-if="scope.row.PlanStatus === '待下发'">{{ scope.row.PlanStatus }}</span>
                      <span class="color-darkblue" v-if="scope.row.PlanStatus === '已下发'">{{ scope.row.PlanStatus }}</span>
                    </template>
                  </el-table-column>
                  <el-table-column label="操作">
                    <template slot-scope="scope">
                      <el-button
                        size="mini"
                        type='primary'
                        @click="Eqconfig(scope.$index, scope.row)">生产配置</el-button>
                    </template>
                  </el-table-column>
              </el-table>
              <div class="paginationClass">
                  <el-pagination background  layout="total,prev, pager, next, jumper"
                  :total="xfTableData.total"
                  :current-page="xfTableData.offset"
                  :page-size="xfTableData.limit"
                  @size-change="xfHandleSizeChange"
                  @current-change="xfHandleCurrentChange">
                  </el-pagination>
            </div>
            <el-dialog title="工艺段配置计划" :visible.sync="dialogTableVisible" width='95%'>
              <el-row>
              <el-col :span='4'>
                  <el-steps :active="configactive" direction="vertical" finish-status="wait" space='100px'>
                    <el-step title="基础配置" @click.native="Activeconfig(0)"></el-step>
                    <el-step v-for='(item,index) in inProcessList' :key='index' :title="item.PUName" @click.native="Activeconfig(index+1)"></el-step>
                  </el-steps>
              </el-col>
              <el-col :span='20' v-if='configactive===0'>
                  <div style="fontSize:18px;fontWeight:700;">备料配置</div>
                  <el-row style="marginTop:24px;">
                    <el-col :span='19'>
                      <el-checkbox v-model="blSelected" style="marginRight:20px;"></el-checkbox>
                      <el-date-picker
                        v-model="blstartTime"
                        value-format='yyyy-MM-dd'
                        type="date"
                        size='small'
                        placeholder="选择日期">
                      </el-date-picker>
                      <el-radio-group v-model="blstartBc" size="small">
                          <el-radio-button label="早"></el-radio-button>
                          <el-radio-button label="中"></el-radio-button>
                          <el-radio-button label="晚"></el-radio-button>
                      </el-radio-group>
                      <span style="margin:0 30px;">至</span>
                            <el-date-picker
                              v-model="blendTime"
                              value-format='yyyy-MM-dd'
                              type="date"
                              size='small'
                              placeholder="选择日期">
                            </el-date-picker>
                            <el-radio-group v-model="blendBc" size="small">
                              <el-radio-button label="早"></el-radio-button>
                              <el-radio-button label="中"></el-radio-button>
                              <el-radio-button label="晚"></el-radio-button>
                            </el-radio-group>
                    </el-col>
                    <el-col :span='4'>
                      <span class="mgr">批量</span>
                      <el-tag type='info'>{{BatchWeight}}</el-tag>
                    </el-col>
                    </el-row>
              </el-col>
              <el-col v-for='(item,index) in inProcessList' :key='index+1' :span='20'>
                <el-col v-if='configactive===index+1'>
                    <div style="fontSize:18px;fontWeight:700;">{{item.PUName}}配置</div>
                    <el-row style="marginTop:24px;">
                      <el-col :span='24' style="marginTop:18px;">
                        <el-row>
                          <el-col :span='24'  v-for="(item,index) in inProcessList[index].eqList" :key='index' class="marginBottom">
                            <el-checkbox v-model="item.isSelected"></el-checkbox>
                            <span style="margin:0 30px;">{{item.EQPCode}}</span>
                            <span style="margin:0 30px;">{{item.EQPName}}</span>
                            <el-date-picker
                              v-model="item.StartTime"
                              value-format='yyyy-MM-dd'
                              type="date"
                              size='small'
                              @change="judgeConflict(item.EQPCode,item.StartTime,item.StartBC)"
                              placeholder="选择日期">
                            </el-date-picker>
                            <el-radio-group v-model="item.StartBC" size="small" @change='judgeConflict(item.EQPCode,item.StartTime,item.StartBC)'>
                              <el-radio-button label="早"></el-radio-button>
                              <el-radio-button label="中"></el-radio-button>
                              <el-radio-button label="晚"></el-radio-button>
                            </el-radio-group>
                            <span style="margin:0 30px;">至</span>
                            <el-date-picker
                              v-model="item.EndTime"
                              value-format='yyyy-MM-dd'
                              type="date"
                              size='small'
                              @change="judgeConflict(item.EQPCode,item.EndTime,item.EndBC)"
                              placeholder="选择日期">
                            </el-date-picker>
                            <el-radio-group v-model="item.EndBC" size="small" @change="judgeConflict(item.EQPCode,item.EndTime,item.EndBC)">
                              <el-radio-button label="早"></el-radio-button>
                              <el-radio-button label="中"></el-radio-button>
                              <el-radio-button label="晚"></el-radio-button>
                            </el-radio-group>
                          </el-col>
                        </el-row>
                      </el-col>
                    </el-row>
                </el-col>
              </el-col>
              </el-row>
              <span slot="footer" class="dialog-footer">
              <el-button @click="dialogTableVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveSelectedEq">保存</el-button>
              </span>
              <el-dialog title="冲突信息" :visible.sync="ctdialogTableVisible" width='80%' :modal=false>
                  <el-table :data="ctlist" class="ctTable">
                    <el-table-column v-for="item in tipstableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width' style='color:red;'></el-table-column>
                  </el-table>
                  <span slot="footer" class="dialog-footer">
                    <el-button type="primary" @click="ctdialogTableVisible = false" size='small'>确 定</el-button>
                  </span>
              </el-dialog>

            </el-dialog>
        </el-col>

        <el-col :span='24' class="platformContainer" v-if="radio3==='撤回'">
           <div style="height:40px;fontSize:16px;fontWeight:700;">撤回列表</div>
              <el-table
                  :data="chTableData.data"
                  highlight-current-row
                  size='small'
                  border
                  ref="chmultipleTable"
                  @row-click="chTabCurrentChange"
                  style="width: 100%">
                  <el-table-column v-for="item in batchtableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
                  <el-table-column prop="PlanStatus" label="计划状态">
                    <template slot-scope="scope">
                      <span class="color-red" v-if="scope.row.PlanStatus === '审核未通过'">{{ scope.row.PlanStatus }}</span>
                      <span class="color-orange" v-if="scope.row.PlanStatus === '待审核'">{{ scope.row.PlanStatus }}</span>
                      <span class="color-purple" v-if="scope.row.PlanStatus === '待配置'">{{ scope.row.PlanStatus }}</span>
                      <span class="color-red" v-if="scope.row.PlanStatus === '撤回'">{{ scope.row.PlanStatus }}</span>
                      <span class="color-darkblue" v-if="scope.row.PlanStatus === '已下发'">{{ scope.row.PlanStatus }}</span>
                    </template>
                  </el-table-column>
                  <el-table-column label="操作">
                    <template slot-scope="scope">
                      <el-button
                        size="mini"
                        type='primary'
                        @click="Eqconfig(scope.$index, scope.row)">生产配置</el-button>
                    </template>
                  </el-table-column>
              </el-table>
              <div class="paginationClass">
                  <el-pagination background  layout="total,prev, pager, next, jumper"
                  :total="chTableData.total"
                  :current-page="chTableData.offset"
                  :page-size="chTableData.limit"
                  @size-change="chHandleSizeChange"
                  @current-change="chHandleCurrentChange">
                  </el-pagination>
            </div>
            <el-dialog title="工艺段配置计划" :visible.sync="dialogTableVisible" width='95%'>
              <el-row>
              <el-col :span='4'>
                  <el-steps :active="configactive" direction="vertical" finish-status="wait" space='100px'>
                    <el-step title="基础配置" @click.native="Activeconfig(0)"></el-step>
                    <el-step v-for='(item,index) in inProcessList' :key='index' :title="item.PUName" @click.native="Activeconfig(index+1)"></el-step>
                  </el-steps>
              </el-col>
              <el-col :span='20' v-if='configactive===0'>
                  <div style="fontSize:18px;fontWeight:700;">备料配置</div>
                  <el-row style="marginTop:24px;">
                    <el-col :span='19'>
                      <el-checkbox v-model="blSelected" style="marginRight:20px;"></el-checkbox>
                      <el-date-picker
                        v-model="blstartTime"
                        value-format='yyyy-MM-dd'
                        type="date"
                        size='small'
                        placeholder="选择日期">
                      </el-date-picker>
                      <el-radio-group v-model="blstartBc" size="small">
                          <el-radio-button label="早"></el-radio-button>
                          <el-radio-button label="中"></el-radio-button>
                          <el-radio-button label="晚"></el-radio-button>
                      </el-radio-group>
                      <span style="margin:0 30px;">至</span>
                            <el-date-picker
                              v-model="blendTime"
                              value-format='yyyy-MM-dd'
                              type="date"
                              size='small'
                              placeholder="选择日期">
                            </el-date-picker>
                            <el-radio-group v-model="blendBc" size="small">
                              <el-radio-button label="早"></el-radio-button>
                              <el-radio-button label="中"></el-radio-button>
                              <el-radio-button label="晚"></el-radio-button>
                            </el-radio-group>
                    </el-col>
                    <el-col :span='4'>
                      <span class="mgr">批量</span>
                      <el-tag type='info'>{{BatchWeight}}</el-tag>
                    </el-col>
                    </el-row>
              </el-col>
              <el-col v-for='(item,index) in inProcessList' :key='index+1' :span='20'>
                <el-col v-if='configactive===index+1'>
                    <div style="fontSize:18px;fontWeight:700;">{{item.PUName}}配置</div>
                    <el-row style="marginTop:24px;">
                      <el-col :span='24' style="marginTop:18px;">
                        <el-row>
                          <el-col :span='24'  v-for="(item,index) in inProcessList[index].eqList" :key='index' class="marginBottom">
                            <el-checkbox v-model="item.isSelected"></el-checkbox>
                            <span style="margin:0 30px;">{{item.EQPCode}}</span>
                            <span style="margin:0 30px;">{{item.EQPName}}</span>
                            <el-date-picker
                              v-model="item.StartTime"
                              value-format='yyyy-MM-dd'
                              type="date"
                              size='small'
                              @change="judgeConflict(item.EQPCode,item.StartTime,item.StartBC)"
                              placeholder="选择日期">
                            </el-date-picker>
                            <el-radio-group v-model="item.StartBC" size="small" @change='judgeConflict(item.EQPCode,item.StartTime,item.StartBC)'>
                              <el-radio-button label="早"></el-radio-button>
                              <el-radio-button label="中"></el-radio-button>
                              <el-radio-button label="晚"></el-radio-button>
                            </el-radio-group>
                            <span style="margin:0 30px;">至</span>
                            <el-date-picker
                              v-model="item.EndTime"
                              value-format='yyyy-MM-dd'
                              type="date"
                              size='small'
                              @change="judgeConflict(item.EQPCode,item.EndTime,item.EndBC)"
                              placeholder="选择日期">
                            </el-date-picker>
                            <el-radio-group v-model="item.EndBC" size="small" @change="judgeConflict(item.EQPCode,item.EndTime,item.EndBC)">
                              <el-radio-button label="早"></el-radio-button>
                              <el-radio-button label="中"></el-radio-button>
                              <el-radio-button label="晚"></el-radio-button>
                            </el-radio-group>
                          </el-col>
                        </el-row>
                      </el-col>
                    </el-row>
                </el-col>
              </el-col>
              </el-row>
              <span slot="footer" class="dialog-footer">
              <el-button @click="dialogTableVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveSelectedEq">保存</el-button>
              </span>
              <el-dialog title="冲突信息" :visible.sync="ctdialogTableVisible" width='80%' :modal=false>
                  <el-table :data="ctlist" class="ctTable">
                    <el-table-column v-for="item in tipstableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
                  </el-table>
                  <span slot="footer" class="dialog-footer">
                    <el-button type="primary" @click="ctdialogTableVisible = false" size='small'>确 定</el-button>
                  </span>
              </el-dialog>
            </el-dialog>
        </el-col>

        <el-col :span='24' class="platformContainer">
           <div style="height:40px;fontSize:16px;fontWeight:700;">配置更改列表</div>
              <el-table
                  :data="eqlistTableData.data"
                  highlight-current-row
                  size='small'
                  border
                  ref="xfmultipleTable"
                  @row-click="xfTabCurrentChange"
                  style="width: 100%">
                  <el-table-column v-for="item in batchtableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
                  <el-table-column prop="PlanStatus" label="计划状态">
                    <template slot-scope="scope">
                      <span class="color-red" v-if="scope.row.PlanStatus === '审核未通过'">{{ scope.row.PlanStatus }}</span>
                      <span class="color-orange" v-if="scope.row.PlanStatus === '待审核'">{{ scope.row.PlanStatus }}</span>
                      <span class="color-purple" v-if="scope.row.PlanStatus === '待配置'">{{ scope.row.PlanStatus }}</span>
                      <span class="color-red" v-if="scope.row.PlanStatus === '撤回'">{{ scope.row.PlanStatus }}</span>
                      <span class="color-lightgreen" v-if="scope.row.PlanStatus === '待下发'">{{ scope.row.PlanStatus }}</span>
                      <span class="color-darkblue" v-if="scope.row.PlanStatus === '已下发'">{{ scope.row.PlanStatus }}</span>
                    </template>
                  </el-table-column>
                  <el-table-column label="操作">
                    <template slot-scope="scope">
                      <el-button
                        size="mini"
                        type='primary'
                        @click="Eqconfig(scope.$index, scope.row)">生产配置</el-button>
                    </template>
                  </el-table-column>
              </el-table>
              <div class="paginationClass">
                  <el-pagination background  layout="total,prev, pager, next, jumper"
                  :total="xfTableData.total"
                  :current-page="xfTableData.offset"
                  :page-size="xfTableData.limit"
                  @size-change="xfHandleSizeChange"
                  @current-change="xfHandleCurrentChange">
                  </el-pagination>
            </div>
            <el-dialog title="工艺段配置计划" :visible.sync="dialogTableVisible" width='95%'>
              <el-row >
              <el-col :span='4'>
                  <el-steps :active="configactive" direction="vertical" finish-status="wait" space='100px'>
                    <el-step title="基础配置" @click.native="Activeconfig(0)"></el-step>
                    <el-step v-for='(item,index) in inProcessList' :key='index' :title="item.PUName" @click.native="Activeconfig(index+1)"></el-step>
                  </el-steps>
              </el-col>
              <el-col :span='20' v-if='configactive===0'>
                  <div style="fontSize:18px;fontWeight:700;">备料配置</div>
                  <el-row style="marginTop:24px;">
                    <el-col :span='19'>
                      <el-checkbox v-model="blSelected" style="marginRight:20px;"></el-checkbox>
                      <el-date-picker
                        v-model="blstartTime"
                        value-format='yyyy-MM-dd'
                        type="date"
                        size='small'
                        placeholder="选择日期">
                      </el-date-picker>
                      <el-radio-group v-model="blstartBc" size="small">
                          <el-radio-button label="早"></el-radio-button>
                          <el-radio-button label="中"></el-radio-button>
                          <el-radio-button label="晚"></el-radio-button>
                      </el-radio-group>
                      <span style="margin:0 30px;">至</span>
                            <el-date-picker
                              v-model="blendTime"
                              value-format='yyyy-MM-dd'
                              type="date"
                              size='small'
                              placeholder="选择日期">
                            </el-date-picker>
                            <el-radio-group v-model="blendBc" size="small">
                              <el-radio-button label="早"></el-radio-button>
                              <el-radio-button label="中"></el-radio-button>
                              <el-radio-button label="晚"></el-radio-button>
                            </el-radio-group>
                    </el-col>
                    <el-col :span='4'>
                      <span class="mgr">批量</span>
                      <el-tag type='info'>{{BatchWeight}}</el-tag>
                    </el-col>
                    </el-row>
              </el-col>
              <el-col v-for='(item,index) in inProcessList' :key='index+1' :span='20'>
                <el-col v-if='configactive===index+1'>
                    <div style="fontSize:18px;fontWeight:700;">{{item.PUName}}配置</div>
                    <el-row style="marginTop:24px;">
                      <el-col :span='24' style="marginTop:18px;">
                        <el-row>
                          <el-col :span='24'  v-for="(item,index) in inProcessList[index].eqList" :key='index' class="marginBottom">
                            <el-checkbox v-model="item.isSelected"></el-checkbox>
                            <span style="margin:0 30px;">{{item.EQPCode}}</span>
                            <span style="margin:0 30px;">{{item.EQPName}}</span>
                            <el-date-picker
                              v-model="item.StartTime"
                              value-format='yyyy-MM-dd'
                              type="date"
                              size='small'
                              @change="judgeConflict(item.EQPCode,item.StartTime,item.StartBC)"
                              placeholder="选择日期">
                            </el-date-picker>
                            <el-radio-group v-model="item.StartBC" size="small" @change='judgeConflict(item.EQPCode,item.StartTime,item.StartBC)'>
                              <el-radio-button label="早"></el-radio-button>
                              <el-radio-button label="中"></el-radio-button>
                              <el-radio-button label="晚"></el-radio-button>
                            </el-radio-group>
                            <span style="margin:0 30px;">至</span>
                            <el-date-picker
                              v-model="item.EndTime"
                              value-format='yyyy-MM-dd'
                              type="date"
                              size='small'
                              @change="judgeConflict(item.EQPCode,item.EndTime,item.EndBC)"
                              placeholder="选择日期">
                            </el-date-picker>
                            <el-radio-group v-model="item.EndBC" size="small" @change="judgeConflict(item.EQPCode,item.EndTime,item.EndBC)">
                              <el-radio-button label="早"></el-radio-button>
                              <el-radio-button label="中"></el-radio-button>
                              <el-radio-button label="晚"></el-radio-button>
                            </el-radio-group>
                          </el-col>
                        </el-row>
                      </el-col>
                    </el-row>
                </el-col>
              </el-col>
              </el-row>
              <span slot="footer" class="dialog-footer">
              <el-button @click="dialogTableVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveSelectedEq">保存</el-button>
              </span>
              <el-dialog title="冲突信息" :visible.sync="ctdialogTableVisible" width='80%' :modal=false>
                  <el-table :data="ctlist" class="ctTable">
                    <el-table-column v-for="item in tipstableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width' class="color-red"></el-table-column>
                  </el-table>
                  <span slot="footer" class="dialog-footer">
                    <el-button type="primary" @click="ctdialogTableVisible = false" size='small'>确 定</el-button>
                  </span>
              </el-dialog>
            </el-dialog>
        </el-col>
       </el-row>
       <el-row v-if="steps===2">
           <el-col :span='24' class="platformContainer">
           <div style="height:40px;fontSize:16px;fontWeight:700;">待下发列表</div>
              <el-table
                  :data="eqlistTableData.data"
                  highlight-current-row
                  size='small'
                  border
                  ref="eqlistmultipleTable"
                  style="width: 100%">
                  <el-table-column v-for="item in eqlistableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
                  <el-table-column prop="PlanStatus" label="计划状态">
                    <template slot-scope="scope">
                      <span class="color-red" v-if="scope.row.PlanStatus === '审核未通过'">{{ scope.row.PlanStatus }}</span>
                      <span class="color-orange" v-if="scope.row.PlanStatus === '待审核'">{{ scope.row.PlanStatus }}</span>
                      <span class="color-purple" v-if="scope.row.PlanStatus === '待配置'">{{ scope.row.PlanStatus }}</span>
                      <span class="color-red" v-if="scope.row.PlanStatus === '撤回'">{{ scope.row.PlanStatus }}</span>
                      <span class="color-lightgreen" v-if="scope.row.PlanStatus === '待下发'">{{ scope.row.PlanStatus }}</span>
                      <span class="color-darkblue" v-if="scope.row.PlanStatus === '已下发'">{{ scope.row.PlanStatus }}</span>
                    </template>
                  </el-table-column>
                  <el-table-column label="操作" fixed="right" width='160'>
                    <template slot-scope="scope">
                      <el-button
                        size="mini"
                        type='success'
                        @click="xfPlan(scope.$index, scope.row)">下发</el-button>
                      <el-button
                        size="mini"
                        type="primary"
                        @click="chPlan(scope.$index, scope.row)">撤回</el-button>
                    </template>
                  </el-table-column>
              </el-table>
              <div class="paginationClass">
                  <el-pagination background  layout="total,prev, pager, next, jumper"
                  :total="eqlistTableData.total"
                  :current-page="eqlistTableData.offset"
                  :page-size="eqlistTableData.limit"
                  @size-change="eqlistHandleSizeChange"
                  @current-change="eqlistHandleCurrentChange">
                  </el-pagination>
            </div>
        </el-col>
           <el-col :span='24' class="platformContainer">
           <div style="height:40px;fontSize:16px;fontWeight:700;">已下发列表</div>
              <el-table
                  :data="yxfbatchTableData.data"
                  highlight-current-row
                  size='small'
                  border
                  style="width: 100%">
                  <el-table-column v-for="item in eqlistableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
                  <el-table-column prop="PlanStatus" label="计划状态">
                    <template slot-scope="scope">
                      <span class="color-red" v-if="scope.row.PlanStatus === '审核未通过'">{{ scope.row.PlanStatus }}</span>
                      <span class="color-orange" v-if="scope.row.PlanStatus === '待审核'">{{ scope.row.PlanStatus }}</span>
                      <span class="color-purple" v-if="scope.row.PlanStatus === '待配置'">{{ scope.row.PlanStatus }}</span>
                      <span class="color-red" v-if="scope.row.PlanStatus === '撤回'">{{ scope.row.PlanStatus }}</span>
                      <span class="color-lightgreen" v-if="scope.row.PlanStatus === '待下发'">{{ scope.row.PlanStatus }}</span>
                      <span class="color-darkblue" v-if="scope.row.PlanStatus === '已下发'">{{ scope.row.PlanStatus }}</span>
                    </template>
                  </el-table-column>
              </el-table>
              <div class="paginationClass">
                  <el-pagination background  layout="total,prev, pager, next, jumper"
                  :total="yxfbatchTableData.total"
                  :current-page="yxfbatchTableData.offset"
                  :page-size="yxfbatchTableData.limit"
                  @size-change="yxfbatchHandleSizeChange"
                  @current-change="yxfbatchHandleCurrentChange">
                  </el-pagination>
            </div>
        </el-col>
       </el-row>
    </el-col>
  </el-row>
</template>

<script>
var moment=require('moment')
  export default {
    name: "planningScheduling",
    data(){
      return {
        steps:0,
        radio3:'待配置',
        configactive:0,
        batchTableData:{ //批次列表
            tableName:"PlanManager",
            data:[],
            limit: 10,//当前显示多少条
            offset: 1,//当前处于多少页
            total: 0,//总的多少页
        },
        xfTableData:{ //待配置批次列表
            tableName:"PlanManager",
            data:[],
            limit: 10,
            offset: 1,
            total: 0,
        },
        chTableData:{ //撤回批次列表
            tableName:"PlanManager",
            data:[],
            limit: 10,
            offset: 1,
            total: 0,
        },
        eqlistTableData:{ //下发批次列表
            tableName:"PlanManager",
            data:[],
            limit: 10,
            offset: 1,
            total: 0,
        },
        yxfbatchTableData:{ //下发批次列表
            tableName:"PlanManager",
            data:[],
            limit: 10,
            offset: 1,
            total: 0,
        },
        BrandCode:'',
        BatchID:'',
        blstartBc:'',//备料开始班次
        blendBc:'',//备料结束班次
        blstartTime:'', //备料开始时间
        blendTime:'', //备料结束时间`,
        blSelected:false,
        ID:0,
        PlanNum:'',
        BatchID:'',
        BrandCode1:'',//getEq中的
        ctdialogTableVisible:false,//冲突显示
        ctlist:[],//冲突存储
        dialogTableVisible:false, //选择设备显示
        xfdialogVisible:false,//是否下发弹框
        inProcessList:[],//存储工序设备集合
        BatchWeight:'200片',
        row:{},
        datalist:[],
        checkedRow:[],//勾选的原生数组
        batchtableconfig:[{prop:'PlanNum',label:"计划单号"},{prop:'BatchID',label:'批次号'},{prop:'BrandCode',label:'品名编码'},{prop:'BrandName',label:'品名'},{prop:'BrandType',label:'产品类型'},{prop:'PlanQuantity',label:'每批产量'},{prop:'Unit',label:'单位'}],//批次列表
        eqlistableconfig:[{prop:'PlanNum',label:"计划单号"},{prop:'BatchID',label:'批次号'},{prop:'BrandCode',label:'品名编码'},{prop:'BrandName',label:'品名'},{prop:'BrandType',label:'产品类型'},{prop:'PlanQuantity',label:'每批产量'},{prop:'Unit',label:'单位'}],//选择设备列表
        tipstableconfig:[{prop:'BatchID',label:"冲突批次号"},{prop:'BrandName',label:'冲突品名'},{prop:'EQPName',label:'冲突设备名称'},{prop:'EQPCode',label:'冲突设备编码'},{prop:'StartTime',label:'冲突开始运行时间'},{prop:'EndTime',label:'冲突结束运行时间'},{prop:'StartBC',label:'冲突开始运行班次'},{prop:'EndBC',label:'冲突结束运行班次'}],//冲突列表
      }
    },
    created(){
      this.getPlanManager()
    },
    mounted(){
    },
    methods:{
      getYxfBatch(){
        var params={
          tableName:'PlanManager',
          PlanStatus:'已下发',
          offset:this.yxfbatchTableData.offset-1,
          limit:this.yxfbatchTableData.limit,
        }
        this.axios.get('/api/CUID',{params:params}).then(res => {
           if(res.data.code === "200"){
            var data = res.data.data
            this.yxfbatchTableData.data = data.rows
            this.yxfbatchTableData.total = data.total
          }
          },err=>{
            console.log("请求错误")
          })

      },
      setStatus(e){
        this.radio3=e
      },
      searchWhyNopass(index,row){
         this.$alert(row.Description, '原因', {
          confirmButtonText: '知道了',
          callback: action => {
            
          }
        });

      },
      judgeConflict(EQPCode,time,Bc){ //判断冲突
       var params={
         EQPCode:EQPCode,
         DateTime:moment(time).format('YYYY-MM-DD'),
         BCType:Bc,
         PlanNum:this.PlanNum,
         BatchID:this.BatchID,
         BrandCode:this.BrandCode1
       }
       this.axios.get('/api/batchconflictequimentselect',{params:params}).then((res) => {
         if(res.data.code==='200'){
           var arr=res.data.data
           if(arr.length!==0){
             this.ctdialogTableVisible=true
             this.ctlist=arr
           }
         }
       })
      },
      saveSelectedEq(){ //保存所选设备触发
        this.dialogTableVisible = false
        var params={
          PUCode: "1038",
          PUName: "备料",
          Seq: 0,
          eqList:[{
            isSelected:this.blSelected,   
            EndBC:this.blendBc,
            EndTime:this.blendTime,
            StartBC:this.blstartBc,
            StartTime:this.blstartTime
          }]
        }
        this.inProcessList.unshift(params)
        var params={
          processList:JSON.stringify(this.inProcessList),
          ID:this.ID
        }
        this.axios.post('/api/addEquipmentBatchRunTime',this.qs.stringify(params)).then((res) => {
          if(res.data.code==='200'){
            this.$message({
              type:'success',
              message:res.data.message
            })
            this.getConfigbatch()
            this.getSelectedEq()
            this.chConfigbatch()
          }else{
            this.$message({
              type:'error',
              message:'获取数据失败'
            })
          }
        })
      },
      getEq(BatchID,BrandCode){ //获取设备
         var params = {
                BatchID: BatchID,
                BrandCode:BrandCode
            }
            this.axios.get("/api/batchequimentselect",{
                params: params
            }).then(res => {
                if(res.data.code === "200"){
                function compare(property){
                    return function(a,b){
                    var value1 = a[property];
                    var value2 = b[property];
                    return value1 - value2;
                    }
                }
                this.inProcessList = res.data.data.processList.sort(compare('Seq'))
                }})
      },
      getSelectedEq(){    //  查询完成设备选择的批次信息
        var params={
          tableName:this.eqlistTableData.tableName,
          PlanStatus:'待下发',
          offset:this.eqlistTableData.offset-1,
          limit:this.eqlistTableData.limit,
        }
        this.axios.get('/api/CUID',{params:params}).then(res => {
           if(res.data.code === "200"){
            var data = res.data.data
            this.eqlistTableData.data = data.rows
            this.eqlistTableData.total = data.total
          }
          },err=>{
            console.log("请求错误")
          })
      },
      xfPlan(index,row){
        var id=row.ID
        var params={
          PlanStatus:'已下发',
          ID:id
        }
        this.$confirm('此操作将下发执行此批次, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
        this.axios.post('/api/createZYPlanZYtask',this.qs.stringify(params)).then((res) => {
          if(res.data.code==='200'){
            this.getSelectedEq()
            this.getYxfBatch()
            this.$message({
              type:'success',
              message:res.data.message
            })
          }else{
            this.$message({
              type:'error',
              message:'下发失败,请重试'
            })
          }
        })},()=>{
          this.$message({
              type:'info',
              message:'已取消操作'
            })
        })
      },
      chPlan(index,row){
        var id=row.ID
        var params={
          PlanStatus:'撤回',
          ID:id
        }
        this.$confirm('此操作将撤回此批次, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
        this.axios.post('/api/createZYPlanZYtask',this.qs.stringify(params)).then((res) => {
          if(res.data.code==='200'){
            this.getSelectedEq()
            this.$message({
              type:'success',
              message:res.data.message
            })
          }else{
            this.$message({
              type:'error',
              message:'撤回失败,请重试'
            })
          }
        })},()=>{
           this.$message({
              type:'info',
              message:'已取消操作'
            })
        })
      },
      Activeconfig(index){ //配置进度条设置
          this.configactive=index
      },
      Eqconfig(){//点击设备配置
        this.dialogTableVisible=true
      },
      checkPass(index,row){
        var id=row.ID
        this.BatchID=row.BatchID
        this.BrandCode=row.BrandCode
        this.$confirm('此操作将审核通过此批次, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
           var params={
            PlanStatus:'待配置',
            Describtion:'',
            ID:id
          }
          this.axios.post('/api/checkPlanManagerSingle',this.qs.stringify(params)).then((res) => {
            if(res.data.code==='200'){
              this.getPlanManager()
               this.$message({
                type: 'success',
                message: '审核成功'
              });
              this.getPlanManager()
            }
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消'
          });          
        });
      },
      checkNopass(index,row){
        var id=row.ID
        this.$prompt('请输入未通过的原因', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          inputType:'text',
        }).then(({ value }) => {
          var params={
            PlanStatus:'审核未通过',
            Describtion:value,
            ID:id
          }
          this.axios.post('/api/checkPlanManagerSingle',this.qs.stringify(params)).then((res) => {
            if(res.data.code==='200'){
              this.getPlanManager()
               this.$message({
                type: 'success',
                message: '提交成功'
              });
               this.getPlanManager()
            }else{
                this.$message({
                type: 'error',
                message: '提交失败，请重试'
              });
            }
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '取消输入'
          });       
        });
      },
      toStep(index){
          this.steps=index
        if(this.steps===0){
          this.getPlanManager()
        }else if(this.steps===1){
          this.getConfigbatch()
          this.chConfigbatch()
          this.getSelectedEq()
        }else if(this.steps===2){
            this.getSelectedEq()
            this.getYxfBatch()
        }else{

        }
      },
      getPlanManager(){ //获取批次列表
        var params={
          tableName:'PlanManager',
          offset:this.batchTableData.offset-1,
          limit:this.batchTableData.limit,
        }
        this.axios.get('/api/CUID',{params:params}).then(res => {
           if(res.data.code === "200"){
            var data = res.data.data
            this.batchTableData.data = data.rows
            this.batchTableData.total = data.total
          }
          },err=>{
            console.log("请求错误")
          })
      },
      getConfigbatch(){ //待配置列表配置
         var params={
          tableName:'PlanManager',
          offset:this.xfTableData.offset-1,
          limit:this.xfTableData.limit,
          PlanStatus:'待配置'
        }
        this.axios.get('/api/CUID',{params:params}).then(res => {
           if(res.data.code === "200"){
            var data = res.data.data
            this.xfTableData.data = data.rows
            this.xfTableData.total = data.total
          }
          },err=>{
            console.log("请求错误")
          })
      },
      chConfigbatch(){ //撤回列表配置
         var params={
          tableName:'PlanManager',
          offset:this.chTableData.offset-1,
          limit:this.chTableData.limit,
          PlanStatus:'撤回'
        }
        this.axios.get('/api/CUID',{params:params}).then(res => {
           if(res.data.code === "200"){
            var data = res.data.data
            this.chTableData.data = data.rows
            this.chTableData.total = data.total
          }
          },err=>{
            console.log("请求错误")
          })
      },
      getBatchWeight(BrandCode,BrandName){ //获取品名表的BatchWeight
        var params={
          tableName:'ProductRule'
        }
        this.axios.get('/api/CUID',{params:params}).then((res) => {
          var arr=res.data.data.rows
          arr.forEach((item) => {
            if(item.BrandName===BrandName){
             this.BatchWeight=item.BatchWeight+item.Unit
            }
          })
        })
      },
      batchHandleSizeChange(limit){ //批次计划 每页条数切换
        this.batchTableData.limit = limit
        this.getPlanManager()
      },
       batchHandleCurrentChange(offset) { //批次计划 页码切换
        this.batchTableData.offset = offset
        this.getPlanManager()
      },
       xfTabCurrentChange(e){ //下发批次计划 点击显示当前的tab行显示详细信息
        this.getEq(e.BatchID,e.BrandCode)
        this.PlanNum=e.PlanNum
        this.BatchID=e.BatchID
        this.BrandCode1=e.BrandCode
        this.ID=e.ID
        this.getBatchWeight(e.BrandCode,e.BrandName)
        this.$refs.xfmultipleTable.clearSelection();
        this.$refs.xfmultipleTable.toggleRowSelection(e)
      },
       chTabCurrentChange(e){ //点击撤回批次计划 点击显示当前的tab行显示详细信息
        this.getEq(e.BatchID,e.BrandCode)
        this.ID=e.ID
        this.getBatchWeight(e.BrandCode,e.BrandName)
        this.$refs.chmultipleTable.clearSelection();
        this.$refs.chmultipleTable.toggleRowSelection(e)
      },
      getAllbatchrow(e){ //审核计划批次点击
        this.checkedRow=e
      },
      shMultiplebatch(){ //点击多批次下发
        this.datalist=[]
        var flag=true
        if(this.checkedRow.length===0){
            this.$message({
               type:'info',
               message:'请先勾选要下发的批次'
             })
             return;
        }else{
          this.checkedRow.forEach((item) => {
          if(item.PlanStatus==='待审核'){
            this.datalist.push(item)
          }else{
            flag=false
            this.$message({
               type:'info',
               message:'当前所选批次包含其他状态，请重新选择'
             })
             return;
          }
        })
        if(flag){
        this.datalist=this.datalist.map((item) => {
          return {
            PlanStatus:'待配置',
            Description:'',
            ID:item.ID
                }
        })
        var params={
          datalist:JSON.stringify(this.datalist)
        }
        this.$confirm('是否通过多批次审核, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.axios.post('/api/checkPlanManager',this.qs.stringify(params)).then((res) => {
           if(res.data.code==='200'){
             this.$message({
               type:'success',
               message:'多批次审核成功'
             })
             this.getPlanManager()
           }
         })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消'
          });          
        });
        }}
      },
      xfHandleSizeChange(limit){ //下发批次计划 每页条数切换
        this.xfTableData.limit = limit
        this.getConfigbatch()
      },
       xfHandleCurrentChange(offset) { //下发批次计划 页码切换
        this.xfTableData.offset = offset
        this.getConfigbatch()
      },
      chHandleSizeChange(limit){ //下发批次计划 每页条数切换
        this.chTableData.limit = limit
        this.chConfigbatch()
      },
       chHandleCurrentChange(offset) { //下发批次计划 页码切换
        this.chTableData.offset = offset
        this.chConfigbatch()
       
      },
      eqlistHandleSizeChange(limit){ //已选设备 每页条数切换
        this.eqlistTableData.limit = limit
        this.getSelectedEq()
      },
       eqlistHandleCurrentChange(offset) { //已选设备 页码切换
        this.eqlistTableData.offset = offset
        this.getSelectedEq()
      },
      yxfbatchHandleSizeChange(limit){ //已选设备 每页条数切换
        this.yxfbatchTableData.limit = limit
        this.getYxfBatch()
      },
       yxfbatchHandleCurrentChange(offset) { //已选设备 页码切换
        this.yxfbatchTableData.offset = offset
        this.getYxfBatch()
      }
    }
  }
</script>

<style scoped>
  .container-col{
    display: inline-block;
    clear: both;
    overflow: hidden;
    border:1px solid #228AD5;
    background:#fff;
    border-radius: 4px;
    padding: 0 15px;
    margin-bottom: 15px;
    margin-right: 10px;
    height: 40px;
    line-height: 40px;
    color: #000;
  }
  .pactive{
    background-color:#228AD5;
    color:#fff;
  }
  .mgr{
    font-size:16px;
    font-weight:700;
    margin-right:15px;
  }
</style>
