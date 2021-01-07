<template>
    <el-row :gutter='20'>
        <el-col :span='24' class="mgt24 container mgb10">
            <div class="mgb24 fsz14px">当前批次流程</div>
            <el-steps :active="currentstep" finish-status="success">
                <el-step class="cursor" name='description' v-for="(item,index) in batchinfo" :key='index' :title="item.Status" >
                    <template slot="description" v-if="item.CheckUser">
                        <div><span>姓名：</span><span>{{item.CheckUser}}</span></div>
                        <div><span>时间：</span><span>{{item.CheckDate}}</span></div>
                    </template>
                </el-step>
            </el-steps>
        </el-col>
        <el-col :span='7'>
            <div class="container mgt24" style="height:400px;">
                <el-col :span='24' style="borderBottom:1px solid #ccc;" class="padd15">
                    <span class="fontWet titl" style="display:inline-block;height:40px;lineHeight:36px;">请验单号</span>
                </el-col>
                <el-col :span='24' class="mgt24">
                    <el-table
                        :data="batchTableData.data"
                        size='small'
                        highlight-current-row
                        style="width: 100%"
                        @row-click="handletabClick">
                        <el-table-column v-for="item in batchtableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
                    </el-table>
                    <div class="paginationClass">
                        <el-pagination background  layout="total, prev, pager, next, jumper"
                        :total="batchTableData.total"
                        :current-page="batchTableData.offset"
                        :page-size="batchTableData.limit"
                        @size-change="handleSizeChange"
                        @current-change="handleCurrentChange">
                    </el-pagination>
                    </div>
                </el-col>
            </div>
        </el-col>
        <el-col :span='17'>
            <el-row class="container mgt24">
                <el-col :span='24'>
                    <el-row>
                        <el-col :span='4' class="mgr15 boxshadow">
                           <el-select v-model="searchObj.category" placeholder="物料类">
                                <el-option
                                v-for="item in options"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                                </el-option>
                            </el-select>
                        </el-col>
                        <el-col :span='4' class="mgr15 boxshadow">
                           <el-date-picker
                            v-model="searchObj.registrydate"
                            type="date"
                            placeholder="选择日期">
                           </el-date-picker>
                        </el-col>
                        <el-col :span='3' class="boxshadow req">
                            <el-button type='primary' @click="SearchTab">查询</el-button>
                        </el-col>
                    </el-row>
                </el-col>
            </el-row>
            <el-row class="mgt24">
                 <el-col :span='24' class="container">
                     <div class="mgt24 mgb24">产品留样原始记录</div>
                     <div style="border:1px solid #ccc;paddingTop:26px;">
                            <el-form ref="form" label-width="100px">
                                <el-row>
                                    <el-col :span='11'>
                                        <el-form-item label="品名：">
                                            <el-input v-model="Row.Product" :disabled="true"></el-input>
                                        </el-form-item>
                                    </el-col>
                                    <el-col :span='11'>
                                        <el-form-item label="产品批号：">
                                            <el-input v-model="Row.ProductNumber" :disabled="true"></el-input>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                                <el-row >
                                    <el-col :span='11'>
                                        <el-form-item label="规格：">
                                            <el-input v-model="Row.Specs" :disabled="true"></el-input>
                                        </el-form-item>
                                    </el-col>
                                    <el-col :span='11'>
                                        <el-form-item label="包装规格：">
                                            <el-input v-model="Row.PackSpecs" :disabled="true"></el-input>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                                <el-row >
                                    <el-col :span='11'>
                                        <el-form-item label="理论产量：">
                                            <el-input v-model="Row.TheoreticalYield" :disabled="true"></el-input>
                                        </el-form-item>
                                    </el-col>
                                    <el-col :span='11'>
                                        <el-form-item label="留样数量：">
                                            <el-input v-model="Row.BatchAmount" :disabled="true"></el-input>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                                <el-row >
                                    <el-col :span='11'>
                                        <el-form-item label="留样部门：">
                                            <el-input v-model="Row.BatchDepartment" :disabled="true"></el-input>
                                        </el-form-item>
                                    </el-col>
                                    <el-col :span='11'>
                                        <el-form-item label="留样人：">
                                            <el-input v-model="Row.BatchName" :disabled="true"></el-input>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                                <el-row >
                                    <el-col :span='11'>
                                        <el-form-item label="留样位置：">
                                            <el-input v-model="Row.Position" :disabled="true"></el-input>
                                        </el-form-item>
                                    </el-col>
                                    <el-col :span='11'>
                                        <el-form-item label="留样时间：">
                                            <el-date-picker v-model="Row.BatchTime" type="date" placeholder="选择日期" :disabled="true"></el-date-picker>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                                <el-row >
                                    <el-col :span='11'>
                                        <el-form-item label="经手人：">
                                            <el-input v-model="Row.Handler" :disabled="true"></el-input>
                                        </el-form-item>
                                    </el-col>
                                    <el-col :span='11'>
                                        <el-form-item label="生产日期：">
                                            <el-date-picker v-model="Row.ProductionDate" type="date" placeholder="选择日期" :disabled="true"></el-date-picker>
                                        </el-form-item>
                                    </el-col>
                                </el-row>  
                                <el-row >
                                    <el-col :span='11'>
                                        <el-form-item label="有效日期：">
                                            <el-date-picker v-model="Row.ValidityDate" type="date" placeholder="选择日期" :disabled="true"></el-date-picker>
                                        </el-form-item>
                                    </el-col>
                                    <el-col :span='11'>
                                        <el-form-item label="备注：">
                                            <el-input type="textarea" autosize placeholder="请输入内容" v-model="Row.Comment" :disabled="true"></el-input>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                            </el-form>
                        </div>
                </el-col>
            </el-row>
            <el-col class="mgt24" style="textAlign:right;"><el-button type="primary" @click="ReceiveLYSample" :disabled='xfopt'>确认接收</el-button></el-col>
        </el-col>
    </el-row>
</template>
<script>
var moment=require('moment')
export default {
    data(){
        return {
           Row:{},
           currentstep:5,
           batchinfo:[{Status:'申请'},{Status:'请验审核'},{Status:'取样'},{Status:'接收'},{Status:'分发'},{Status:'留样接收'},{Status:'留样观察'}],
           distribute:{
               CheckProjectNO:'',
           },
           searchObj:{
               category:'玉米淀粉',
               registrydate:moment(new Date()).format('YYYY-MM-DD')
           },
           options: [{
                value: '选项1',
                label: '物料一'
                }],
            batchTableData:{ //物料BOM
                data:[],
                limit: 5,//当前显示多少条
                offset: 1,//当前处于多少页
                total: 0,//总的多少页
            },
            xfopt:true,
            batchtableconfig:[{prop:'ProductNumber',label:'产品批号'},{prop:'Product',label:'品名'},{prop:'BatchTime',label:'留样时间',width:155}],//批次列表
        }
    },
    created(){
       this.getSelectOption()
       this.SearchTab()
    },
    methods: {
        ReceiveLYSample(){ //接收留样记录
            var params2={
              CheckProjectNO:this.distribute.CheckProjectNO,
              Product:this.Row.Name,
              Specs:this.Row.Specs,
              ProductNumber:this.Row.ProductNumber,
              PackSpecs:this.Row.PackSpecs,
              TheoreticalYield:this.Row.TheoreticalYield,
              BatchAmount:this.Row.BatchAmount,
              BatchDepartment:this.Row.BatchDepartment,
              BatchName:this.Row.BatchName,
              Position:this.Row.Position,
              BatchTime:moment(this.Row.BatchTime).format("YYYY-MM-DD"),
              Handler:this.Row.Handler,
              ProductionDate:moment(this.Row.ProductionDate).format("YYYY-MM-DD"),
              ValidityDate:moment(this.Row.ValidityDate).format("YYYY-MM-DD"),
              Comment:this.Row.Comment
            }
            this.axios.post('/lims/ProductSave',this.qs.stringify(params2)).then((res) => {
                if(res.data.code=='1000'){
                    this.$message({
                        type:'success',
                        message:'留样记录接收成功'
                    })
                }else{
                    this.$message({
                        type:'error',
                        message:'留样记录接收失败'
                    })
                }
            })
        },
         getSelectOption() { //获取下拉列表选项
           this.axios.get('/lims/AllProduct').then((res) => {
               if(res.data.code=='1000'){
                  this.options=res.data.data.map((item) => {
                      return {
                          value:item,
                          label:item
                      }
                  })
               }

           })
        },
         SearchTab(){ //查询相关数据
            var params={
                Page:this.batchTableData.offset,
                PerPage:this.batchTableData.limit,
                Product:this.searchObj.category,
                DateTime:moment(this.searchObj.registrydate).format("YYYY-MM-DD"),
                Status:'LY'
            }
            this.axios.get('/lims/ProductSave',{params:params}).then((res) => {
                this.batchTableData.data=res.data.data
                this.batchTableData.total=res.data.total
            })
        },
        handletabClick(row){ //左侧tab点击事件
            this.xfopt=false
            this.Row=row
            this.distribute.CheckProjectNO=row.CheckProjectNO
            this.getCurrentSteps(row.CheckProjectNO)
        },
        getCurrentSteps(CheckProjectNO){ //获取进度条
           var params={
                Action:'p',
                CheckProjectNO:CheckProjectNO
            }
            this.axios.get('/lims/Board',{params:params}).then((res) => {
                if(res.data.code=='1000'){
                   this.currentstep=res.data.data.length
                   this.batchinfo=this.batchinfo.map((item) => { //清空缓存的状态
                       return {Status:item.Status}
                   })
                   this.batchinfo.splice(0,res.data.data.length)
                   this.batchinfo=res.data.data.concat(this.batchinfo)
                }else{
                    this.$message({
                        type:'info',
                        message:'获取数据失败，请重试'
                    })
                }
            })
        },
        handleSizeChange(limit){ //每页条数切换
            this.batchTableData.limit = limit
            this.SearchTab()
      },
        handleCurrentChange(offset) { // 页码切换
            this.batchTableData.offset = offset
            this.SearchTab()
        },
    },
}
</script>
<style scoped>

</style>