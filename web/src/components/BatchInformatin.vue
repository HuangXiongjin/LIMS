<template>
    <div class="platformContainer" style="height:740px;">
        <el-row>
          <el-col :span='24' class="marginBottom"><div style="fontSize:16px;fontWeight:700;">计划详情</div></el-col>
          <el-col :span='24' style="marginBottom:30px;">
            <el-row>
              <el-col :span='3'>
                <div style="paddingBottom:14px;">计划单号</div>
                <div>{{currentSBatch.PlanNum}}</div>
              </el-col>
              <el-col :span='13'>
                 <div style="paddingBottom:14px;">状态</div>
                <div>{{currentSBatch.PlanStatus}}</div>
              </el-col>
              <el-col :span='4'><el-button type="warning" plain>驳回计划</el-button></el-col>
              <el-col :span='4'><el-button type="success" plain>执行计划</el-button></el-col>
            </el-row>
          </el-col>
          <el-col :span='24' class="marginBottom"><div style="fontSize:16px;fontWeight:700;">基础信息</div></el-col>
          <el-col :span='24' style="marginBottom:30px;">
             <el-table
              :data="[currentSBatch]"
              style="width: 100%">
             <el-table-column v-for="item in tableconfig" :width='item.width'  :key='item.prop' :prop='item.prop' :label='item.label'></el-table-column>
            </el-table>
          </el-col>
          <el-col :span='24' class="marginBottom"><div style="fontSize:16px;fontWeight:700;">物料明细</div></el-col>
          <el-col :span='24' class="marginBottom">
            <div width="100%">
               <el-table
                  :data="zhuMaterial"
                  style="width: 100%">
                  <el-table-column v-for="item in zhutableconfig" :key='item.prop' :prop='item.prop' :label='item.label'></el-table-column>
                </el-table>
            </div>
            <div width="100%">
               <el-table
                  :data="fuMaterial"
                  style="width: 100%">
                <el-table-column v-for="item in futableconfig" :key='item.prop' :prop='item.prop' :label='item.label'></el-table-column>
                </el-table>
            </div>
          </el-col>
          <el-col :span='24' class="marginBottom"><div style="fontSize:16px;fontWeight:700;">计划进度</div></el-col>
          <el-col :span='24' class="marginBottom">
            <el-steps :active="1" align-center >
                <el-step  v-for="(item,index) in steps" :title="item.title" :key='index' :description="item.description">
                    <template slot="description" >
                        <span>{{item.startTime}}<br/>{{item.endTime}}</span>
                    </template>
                </el-step>
             </el-steps>
          </el-col>
        </el-row>
      </div>
</template>
<script>
export default {
    props:['currentSBatch'],
    data(){
        return {
            zhuMaterial: [{
            name: '苦参',
            codeNO: 'LPL3451',
            PlanNum:100,
            factNum:109.3,
            storeplace:'AF-JS'
          }],
          fuMaterial: [{
            name: '黄芪',
            codeNO: 'HQrtyy1',
            PlanNum:19.2,
            factNum:19.3,
            storeplace:'LF-JS'
          },{
            name: '白莲',
            codeNO: 'BL0rtyy1',
            PlanNum:79.2,
            factNum:69.3,
            storeplace:'LF-JS'
          }],
            steps:[{title:'计划申请',startTime:'2020-09-09',endTime:"2020-09-10"},{title:'计划申请',startTime:'2020-09-11',endTime:"2020-09-12"},{title:'计划申请',startTime:'2020-09-13',endTime:"2020-09-14"}],
            tableconfig:[{prop:'BatchID',label:"批次号",width:'170'},{prop:'BrandName',label:'品名',width:'90'},{prop:'PlanStatus',label:'计划状态',width:'110'},{prop:'PlanBeginTime',label:'计划开始时间'},{prop:'PlanEndTime',label:'计划完成时间'}],
            zhutableconfig:[{prop:'name',label:"辅料名称"},{prop:'codeNO',label:'辅料编号'},{prop:'PlanNum',label:'计划投料量'},{prop:'factNum',label:'实际投料量'},{prop:'storeplace',label:'来料储柜'}],
            futableconfig:[{prop:'name',label:"辅料名称"},{prop:'codeNO',label:'辅料编号'},{prop:'PlanNum',label:'计划投料量'},{prop:'factNum',label:'实际投料量'},{prop:'storeplace',label:'来料储柜'}],

        }
    },
    methods:{
    }
}
</script>
<style scoped>

</style>