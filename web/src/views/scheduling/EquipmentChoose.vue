<template>
    <el-row>
          <el-col :span='24' class="marginBottom">
            <el-button type="primary" size="small" @click="back">返回主流程</el-button>
            <el-button type="primary" size="small" icon='el-icon-refresh-right' @click="refreshData">刷新</el-button>
            <el-radio-group v-model="radio3" size="small" @change="setStatus">
                <el-radio-button label="待配置"></el-radio-button>
                <el-radio-button label="撤回"></el-radio-button>
            </el-radio-group>
          </el-col>
          <el-col :span='24' class="platformContainer" v-if="radio3==='待配置'">
           <div style="height:40px;fontSize:16px;fontWeight:700;">待配置列表</div>
              <el-table
                  :data="xfTableData.data"
                  highlight-current-row
                  size='small'
                  border
                  ref="xfallmultipleTable"
                  @row-click="xfallTabCurrentChange"
                  style="width: 100%">
                  <el-table-column type="selection" width="55"></el-table-column>
                  <el-table-column v-for="item in batchtableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
                  <el-table-column prop="PlanStatus" label="计划状态">
                    <template slot-scope="scope">
                      <b class="color-red cursor-pointer" v-if="scope.row.PlanStatus === '审核未通过'">{{ scope.row.PlanStatus }}</b>
                      <b class="color-orange" v-if="scope.row.PlanStatus === '待审核'">{{ scope.row.PlanStatus }}</b>
                      <b class="color-purple" v-if="scope.row.PlanStatus === '待配置'">{{ scope.row.PlanStatus }}</b>
                      <b class="color-red" v-if="scope.row.PlanStatus === '撤回'">{{ scope.row.PlanStatus }}</b>
                      <b class="color-lightgreen" v-if="scope.row.PlanStatus === '待下发'">{{ scope.row.PlanStatus }}</b>
                      <b class="color-darkblue" v-if="scope.row.PlanStatus === '已下发'">{{ scope.row.PlanStatus }}</b>
                      <b class="color-brown" v-if="scope.row.PlanStatus === '已发送投料计划'">{{ scope.row.PlanStatus }}</b>
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
                  @size-change="xfallHandleSizeChange"
                  @current-change="xfallHandleCurrentChange">
                  </el-pagination>
            </div>
            <el-dialog title="工艺段配置计划" :visible.sync="dialogTableVisible" width='90%'>
              <el-row>
              <el-col :span='4'>
                  <el-steps :active="configactive" direction="vertical" finish-status="success" space='100px'>
                    <el-step v-for='(item,index) in inProcessList' :key='index' :title="item.PUName"></el-step>
                  </el-steps>
              </el-col>
              <el-col v-for='(item,index) in inProcessList' :key='index' :span='20'>
                <el-col v-if='configactive===index'>
                    <div style="fontSize:18px;fontWeight:700;">{{item.PUName}}配置<span style="marginLeft:10px;fontSize:14px;color:red;">(先选开始时间，再选结束时间,再"√"选设备)</span></div>
                    <!-- 设置默认时间 -->
                      <div class="marginTop">
                      <el-tag>默认时间</el-tag>
                      <el-date-picker
                              v-model="EQdefaultStartTime"
                              value-format='yyyy-MM-dd'
                              type="date"
                              size='small'
                              @change="getdefsTime"
                              placeholder="选择日期">
                      </el-date-picker>
                      <el-radio-group v-model="EQdefaultStartBC" size="small" @change="clearactivedefault">
                              <el-radio-button label="早"></el-radio-button>
                              <el-radio-button label="白"></el-radio-button>
                              <el-radio-button label="中"></el-radio-button>
                      </el-radio-group>
                      <span style="margin:0 30px;">至</span>
                      <el-date-picker
                              v-model="EQdefaultEndTime"
                              value-format='yyyy-MM-dd'
                              type="date"
                              size='small'
                              @change="getdefeTime"
                              placeholder="选择日期">
                      </el-date-picker>
                      <el-radio-group v-model="EQdefaultEndBC" size="small" @change="clearactivedefault">
                              <el-radio-button label="早"></el-radio-button>
                              <el-radio-button label="白"></el-radio-button>
                              <el-radio-button label="中"></el-radio-button>
                      </el-radio-group>
                    </div>
                    <el-row style="marginTop:24px;">
                      <el-col :span='24'>
                        <el-row>
                          <el-col :span='24'  v-for="(item,index) in inProcessList[configactive].eqList" :key='index' class="marginBottom">
                            <el-checkbox v-model="item.isSelected" @change="setDefaultTime(item.isSelected,index,item.EQPCode)">
                                <span style="margin:0 60px;">{{item.EQPCode}}</span>
                                <span style="margin:0 60px;">{{item.EQPName}}</span>
                            </el-checkbox> 
                          </el-col>
                        </el-row>
                      </el-col>
                    </el-row>
                </el-col>
              </el-col>
              </el-row>
              <span slot="footer" class="dialog-footer">
                <el-button @click="dialogTableVisible = false">取 消</el-button>
                <el-button type="primary" @click="lastconfig" v-show="configactive!==0">上一步</el-button>
                <el-button type="primary" @click="nextconfig" v-show="configactive!==inProcessList.length-1" :disabled='compareTime'>下一步</el-button>
                <el-button type="primary" @click="saveSelectedEq" v-show="configactive===inProcessList.length-1">保存</el-button>
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
        <!-- 撤回的列表 -->
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
                  <el-table-column type="selection" width="55"></el-table-column>
                  <el-table-column v-for="item in batchtableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
                  <el-table-column prop="PlanStatus" label="计划状态">
                    <template slot-scope="scope">
                       <b class="color-red cursor-pointer" v-if="scope.row.PlanStatus === '审核未通过'"{{ scope.row.PlanStatus }}</b>
                      <b class="color-orange" v-if="scope.row.PlanStatus === '待审核'">{{ scope.row.PlanStatus }}</b>
                      <b class="color-purple" v-if="scope.row.PlanStatus === '待配置'">{{ scope.row.PlanStatus }}</b>
                      <b class="color-red" v-if="scope.row.PlanStatus === '撤回'">{{ scope.row.PlanStatus }}</b>
                      <b class="color-lightgreen" v-if="scope.row.PlanStatus === '待下发'">{{ scope.row.PlanStatus }}</b>
                      <b class="color-darkblue" v-if="scope.row.PlanStatus === '已下发'">{{ scope.row.PlanStatus }}</b>
                      <b class="color-brown" v-if="scope.row.PlanStatus === '已发送投料计划'">{{ scope.row.PlanStatus }}</b>
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
            <el-dialog title="工艺段配置计划" :visible.sync="dialogTableVisible" width='90%'>
              <el-row>
              <el-col :span='4'>
                  <el-steps :active="configactive" direction="vertical" finish-status="success" space='100px'>
                    <el-step v-for='(item,index) in inProcessList' :key='index' :title="item.PUName"></el-step>
                  </el-steps>
              </el-col>
               <el-col v-for='(item,index) in inProcessList' :key='index' :span='20'>
               <el-col v-if='configactive===index'>
                    <div style="fontSize:18px;fontWeight:700;">{{item.PUName}}配置<span style="marginLeft:10px;fontSize:14px;color:red;">(先选开始时间，再选结束时间,再"√"选设备)</span></div>
                    <!-- 设置默认时间 -->
                      <div class="marginTop">
                      <el-tag>默认时间</el-tag>
                      <el-date-picker
                              v-model="EQdefaultStartTime"
                              value-format='yyyy-MM-dd'
                              type="date"
                              size='small'
                              @change="getdefsTime"
                              placeholder="选择日期">
                      </el-date-picker>
                      <el-radio-group v-model="EQdefaultStartBC" size="small" @change="clearactivedefault">
                              <el-radio-button label="早"></el-radio-button>
                              <el-radio-button label="白"></el-radio-button>
                              <el-radio-button label="中"></el-radio-button>
                      </el-radio-group>
                      <span style="margin:0 30px;">至</span>
                      <el-date-picker
                              v-model="EQdefaultEndTime"
                              value-format='yyyy-MM-dd'
                              type="date"
                              size='small'
                              @change="getdefeTime"
                              placeholder="选择日期">
                      </el-date-picker>
                      <el-radio-group v-model="EQdefaultEndBC" size="small" @change="clearactivedefault">
                              <el-radio-button label="早"></el-radio-button>
                              <el-radio-button label="白"></el-radio-button>
                              <el-radio-button label="中"></el-radio-button>
                      </el-radio-group>
                    </div>
                    <el-row style="marginTop:24px;">
                      <el-col :span='24'>
                        <el-row>
                          <el-col :span='24'  v-for="(item,index) in inProcessList[configactive].eqList" :key='index' class="marginBottom">
                            <el-checkbox v-model="item.isSelected" @change="setDefaultTime(item.isSelected,index,item.EQPCode)">
                                <span style="margin:0 60px;">{{item.EQPCode}}</span>
                                <span style="margin:0 60px;">{{item.EQPName}}</span>
                            </el-checkbox>
                          </el-col>
                        </el-row>
                      </el-col>
                    </el-row>
                </el-col>
              </el-col>
              </el-row>
              <span slot="footer" class="dialog-footer">
                <el-button @click="dialogTableVisible = false">取 消</el-button>
                <el-button type="primary" @click="lastconfig" v-show="configactive!==0">上一步</el-button>
                <el-button type="primary" @click="nextconfig" v-show="configactive!==inProcessList.length-1">下一步</el-button>
                <el-button type="primary" @click="saveSelectedEq" v-show="configactive===inProcessList.length-1">保存</el-button>
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
        <!-- // 分界线-->
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
                  <el-table-column type="selection" width="55"></el-table-column>
                  <el-table-column v-for="item in batchtableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
                  <el-table-column prop="PlanStatus" label="计划状态">
                    <template slot-scope="scope">
                      <b class="color-red cursor-pointer" v-if="scope.row.PlanStatus === '审核未通过'">{{ scope.row.PlanStatus }}</b>
                      <b class="color-orange" v-if="scope.row.PlanStatus === '待审核'">{{ scope.row.PlanStatus }}</b>
                      <b class="color-purple" v-if="scope.row.PlanStatus === '待配置'">{{ scope.row.PlanStatus }}</b>
                      <b class="color-red" v-if="scope.row.PlanStatus === '撤回'">{{ scope.row.PlanStatus }}</b>
                      <b class="color-lightgreen" v-if="scope.row.PlanStatus === '待下发'">{{ scope.row.PlanStatus }}</b>
                      <b class="color-darkblue" v-if="scope.row.PlanStatus === '已下发'">{{ scope.row.PlanStatus }}</b>
                      <b class="color-brown" v-if="scope.row.PlanStatus === '已发送投料计划'">{{ scope.row.PlanStatus }}</b>
                    </template>
                  </el-table-column>
                  <el-table-column label="操作">
                    <template slot-scope="scope">
                      <el-button
                        size="mini"
                        type='primary'
                        @click="dpzEqconfig(scope.$index, scope.row)">生产配置</el-button>
                    </template>
                  </el-table-column>
              </el-table>
              <div class="paginationClass">
                  <el-pagination background  layout="total,prev, pager, next, jumper"
                  :total="eqlistTableData.total"
                  :current-page="eqlistTableData.offset"
                  :page-size="eqlistTableData.limit"
                  @size-change="xfHandleSizeChange"
                  @current-change="xfHandleCurrentChange">
                  </el-pagination>
            </div>
            <el-dialog title="工艺段配置计划" :visible.sync="dpzdialogTableVisible" width='95%'>
              <el-row >
              <el-col :span='4'>
                  <el-steps :active="configactive" direction="vertical" finish-status="success" space='100px'>
                    <el-step v-for='(item,index) in inProcessList' :key='index' :title="item.PUName"></el-step>
                  </el-steps>
              </el-col>
              <el-col v-for='(item,index) in inProcessList' :key='index' :span='20'>
                <el-col v-if='configactive===index'>
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
                              <el-radio-button label="白"></el-radio-button>
                              <el-radio-button label="中"></el-radio-button>
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
                              <el-radio-button label="白"></el-radio-button>
                              <el-radio-button label="中"></el-radio-button>
                            </el-radio-group>
                          </el-col>
                        </el-row>
                      </el-col>
                    </el-row>
                </el-col>
              </el-col>
              </el-row>
              <span slot="footer" class="dialog-footer">
                <el-button @click="dpzdialogTableVisible = false">取 消</el-button>
                <el-button type="primary" @click="lastconfig" v-show="configactive!==0">上一步</el-button>
                <el-button type="primary" @click="nextconfig" v-show="configactive!==inProcessList.length-1">下一步</el-button>
                <el-button type="primary" @click="saveSelectedEq" v-show="configactive===inProcessList.length-1">保存</el-button>
              </span>
              <el-dialog title="冲突信息" :visible.sync="dpzctdialogTableVisible" width='80%' :modal=false>
                  <el-table :data="ctlist" class="ctTable">
                    <el-table-column v-for="item in tipstableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width' class="color-red"></el-table-column>
                  </el-table>
                  <span slot="footer" class="dialog-footer">
                    <el-button type="primary" @click="dpzctdialogTableVisible = false" size='small'>确 定</el-button>
                  </span>
              </el-dialog>
            </el-dialog>
        </el-col>
       </el-row>
</template>>
<script>
var moment=require('moment')
export default {
    data(){
        return {
            radio3:'待配置',
            configactive:0,
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
            eqlistTableData:{ //待下发批次列表
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
            dpzctdialogTableVisible:false,//待配置冲突显示
            dpzdialogTableVisible:false,//待配置显示
            ctlist:[],//冲突存储
            dialogTableVisible:false, //选择设备显示
            inProcessList:[],//存储工序设备集合
            BatchWeight:'200片',
            row:{},
            currentclick:'撤回',
            EQdefaultStartTime:moment().format("YYYY-MM-DD"),
            EQdefaultStartBC:'早',
            EQdefaultEndBC:'早',
            stTime:new Date().getTime(),
            endTL:new Date().getTime(),
            lastendTL:new Date().getTime(),
            compareTime:false,
            EQdefaultEndTime:moment().format("YYYY-MM-DD"),
            batchtableconfig:[{prop:'PlanNum',label:"计划单号"},{prop:'BatchID',label:'批次号'},{prop:'SchedulePlanCode',label:'调度编号'},{prop:'BrandCode',label:'品名编码'},{prop:'BrandName',label:'品名'},{prop:'BrandType',label:'产品类型'},{prop:'PlanQuantity',label:'计划产量'},{prop:'Unit',label:'单位'}],//批次列表
            tipstableconfig:[{prop:'BatchID',label:"冲突批次号"},{prop:'BrandName',label:'冲突品名'},{prop:'EQPName',label:'冲突设备名称'},{prop:'EQPCode',label:'冲突设备编码'},{prop:'StartTime',label:'冲突开始运行时间'},{prop:'EndTime',label:'冲突结束运行时间'},{prop:'StartBC',label:'冲突开始运行班次'},{prop:'EndBC',label:'冲突结束运行班次'}],//冲突列表
        }
    },
    created(){
         this.getConfigbatch()
         this.chConfigbatch()
         this.getSelectedEq()
    },
    methods:{
      initTime(){ //时间数据初始化
        this.EQdefaultStartTime=moment().format("YYYY-MM-DD")
        this.EQdefaultStartBC='早'
        this.EQdefaultEndBC='早'
        this.stTime=new Date().getTime()
        this.endTL=new Date().getTime()
        this.lastendTL=new Date().getTime()
        this.compareTime=false
        this.EQdefaultEndTime=moment().format("YYYY-MM-DD")
      },
      lastconfig(){
        this.configactive--
      },
      nextconfig(){
        this.configactive++
      },
     getdefsTime(e){ //判断开始时间
       this.stTime=new Date(e).getTime()
       this.clearactivedefault()
       if(this.stTime<this.lastendTL){
         this.$message({
              type:'error',
              message:"开始时间小于前步骤工序结束时间，重新选择！"
            })
          this.compareTime=true
       }else{
         this.compareTime=false
       }
       if(this.stTime>this.endTL){
         this.$message({
              type:'warning',
              message:"当前开始时间大于当前结束时间，重新选择！"
            })
          this.compareTime=true
       }else{
         this.compareTime=false
       }
      },
     getdefeTime(e){ //判断结束时间
       this.endTL=new Date(e).getTime()
       this.clearactivedefault()
       if(this.endTL<this.stTime){
         this.$message({
              type:'error',
              message:"当前结束时间小于开始时间，重新选择！"
            })
        this.compareTime=true
       }else{
        this.lastendTL=new Date(e).getTime()
        this.compareTime=false
       }
     },
      refreshData(){ //刷新数据
         this.getConfigbatch()
         this.chConfigbatch()
         this.getSelectedEq()
      },
      cleardefault(){ //清除选择的全部勾选
        this.inProcessList.forEach((item) => {
            var eqlist=item.eqList
            if(eqlist!==[]){
            eqlist.forEach((item1) => {
              item1.isSelected=false
            })}
        })
      },
      clearactivedefault(){ //更换时间班次清除选择
        this.inProcessList[this.configactive].eqList.forEach((item) => {
              item.isSelected=false
        })
      },
      setDefaultTime(e,index,EQPCode){ //勾选设置默认时间
        if(e){
          this.inProcessList[this.configactive].eqList[index].StartTime=this.EQdefaultStartTime
          this.inProcessList[this.configactive].eqList[index].EndTime=this.EQdefaultEndTime
          this.inProcessList[this.configactive].eqList[index].StartBC=this.EQdefaultStartBC
          this.inProcessList[this.configactive].eqList[index].EndBC=this.EQdefaultEndBC
          if(this.configactive!==0){
            this.judgeConflict(EQPCode,this.EQdefaultStartTime,this.EQdefaultStartBC)
            this.judgeConflict(EQPCode,this.EQdefaultEndTime,this.EQdefaultEndBC)

          }
        }else{
          this.inProcessList[this.configactive].eqList[index].StartTime=''
          this.inProcessList[this.configactive].eqList[index].EndTime=''
          this.inProcessList[this.configactive].eqList[index].StartBC=''
          this.inProcessList[this.configactive].eqList[index].EndBC=''
        }
      },
      //点击同步备料信息
      getSelectedBl(){
        var params={
          tableName:'EquipmentBatchRunTime',
          BatchID:this.BatchID,
          BrandCode:this.BrandCode1,
          PUName:'备料'
        }
        this.axios.get('/api/CUID',{params:params}).then((res) => {
          var arr=res.data.data.rows[0]
          if(res.data.data.rows.length===0){
            this.blstartBc=''
            this.blendBc=''
            this.blstartTime=''
            this.blendTime=''
            this.blSelected=false
          }else{
            this.blstartBc=arr.StartBC
            this.blendBc=arr.EndBC
            this.blstartTime=arr.StartTime
            this.blendTime=arr.EndTime
            this.blSelected=true
          }
        })
      },
      forward(){
        this.$router.push('/DistributionPlan')
      },
      back(){ //返回主流程
        this.$router.push('/planProgress')
      },
      setStatus(e){
        this.radio3=e
        if(e==='撤回'){
          this.chConfigbatch()
        }else if(e==='待配置'){
          this.getConfigbatch()
        }
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
             if(this.dpzdialogTableVisible){
               this.dpzctdialogTableVisible=true
             }else{
               this.ctdialogTableVisible=true
             }
             this.ctlist=arr
           }
         }
       })
      },
      saveSelectedEq(){ //保存所选设备触发
        this.dialogTableVisible = false
        this.dpzdialogTableVisible = false
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
                if(this.currentclick==='撤回'){
                  this.cleardefault()
                }
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
      Eqconfig(){//点击设备配置
        this.dialogTableVisible=true
      },
      dpzEqconfig(){//点击设备配置
        this.dpzdialogTableVisible=true
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
       xfallTabCurrentChange(e){ //待配置批次计划 点击显示当前的tab行显示详细信息
        this.configactive=0
        this.currentclick='待配置'
        this.getEq(e.BatchID,e.BrandCode)
        this.initTime()
        this.$refs.xfallmultipleTable.setCurrentRow(e)
        this.PlanNum=e.PlanNum
        this.BatchID=e.BatchID
        this.BrandCode1=e.BrandCode
        this.ID=e.ID
        //备料置空
        this.blstartBc=''
        this.blendBc=''
        this.blstartTime=''
        this.blendTime=''
        this.blSelected=false
        this.getBatchWeight(e.BrandCode,e.BrandName)
        this.$refs.xfallmultipleTable.clearSelection();
        this.$refs.xfallmultipleTable.toggleRowSelection(e)

      },
       xfTabCurrentChange(e){ //配置更改批次计划 点击显示当前的tab行显示详细信息
        this.configactive=0
        this.currentclick='配置更改'
        this.initTime()
        this.getEq(e.BatchID,e.BrandCode)
        this.$refs.xfmultipleTable.setCurrentRow(e)
        this.PlanNum=e.PlanNum
        this.BatchID=e.BatchID
        this.BrandCode1=e.BrandCode
        this.ID=e.ID
        this.getSelectedBl()
        this.getBatchWeight(e.BrandCode,e.BrandName)
        this.$refs.xfmultipleTable.clearSelection();
        this.$refs.xfmultipleTable.toggleRowSelection(e)
      },
       chTabCurrentChange(e){ //点击撤回批次计划 点击显示当前的tab行显示详细信息
       this.configactive=0
        this.currentclick='撤回'
        this.initTime()
        this.getEq(e.BatchID,e.BrandCode)
        this.$refs.chmultipleTable.setCurrentRow(e)
        this.ID=e.ID
        this.blstartBc=''
        this.blendBc=''
        this.blstartTime=''
        this.blendTime=''
        this.blSelected=false
        this.getBatchWeight(e.BrandCode,e.BrandName)
        this.$refs.chmultipleTable.clearSelection();
        this.$refs.chmultipleTable.toggleRowSelection(e)
      },
      xfallHandleSizeChange(limit){ //待配置批次计划 每页条数切换
        this.xfTableData.limit = limit
        this.getConfigbatch()
      },
       xfallHandleCurrentChange(offset) { //待配置批次计划 页码切换
        this.xfTableData.offset = offset
        this.getConfigbatch()
      },
      xfHandleSizeChange(limit){ //已下发批次计划 每页条数切换
        this.eqlistTableData.limit = limit
        this.getSelectedEq()
      },
       xfHandleCurrentChange(offset) { //已下发批次计划 页码切换
        this.eqlistTableData.offset = offset
        this.getSelectedEq()
      },
      chHandleSizeChange(limit){ //撤回批次计划 每页条数切换
        this.chTableData.limit = limit
        this.chConfigbatch()
      },
       chHandleCurrentChange(offset) { //撤回批次计划 页码切换
        this.chTableData.offset = offset
        this.chConfigbatch()
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
    }
  }
</script>
<style scoped>
.mgr{
    font-size:16px;
    font-weight:700;
    margin-right:15px;
  }
</style>