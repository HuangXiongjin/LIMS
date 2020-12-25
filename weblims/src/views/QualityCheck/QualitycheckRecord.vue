<template>
    <el-row :gutter='20'>
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
                        <div class="mgt24 mgb24">检验记录</div>
                        <div style="border:1px solid #ccc;paddingTop:26px;">
                            <el-form ref="form" :model="RecordForm" label-width="100px">
                                <el-row>
                                    <el-col :span='11'>
                                        <el-form-item label="品名：">
                                            <el-input v-model="Row.Name" :disabled="true"></el-input>
                                        </el-form-item>
                                    </el-col>
                                    <el-col :span='11'>
                                        <el-form-item label="批号：">
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
                                        <el-form-item label="请验部门：">
                                            <el-input v-model="Row.CheckDepartment" :disabled="true"></el-input>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                                <el-row >
                                    <el-col :span='11'>
                                        <el-form-item label="剂型：">
                                            <el-input v-model="RecordForm.Type"></el-input>
                                        </el-form-item>
                                    </el-col>
                                    <el-col :span='11'>
                                        <el-form-item label="批数量：">
                                            <el-input v-model="Row.Amount" :disabled="true"></el-input>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                                <el-row >
                                    <el-col :span='11'>
                                        <el-form-item label="取样时间：">
                                            <el-input v-model="Row.VerifyDate" :disabled="true"></el-input>
                                        </el-form-item>
                                    </el-col>
                                    <el-col :span='11'>
                                        <el-form-item label="检验日期：">
                                            <el-input v-model="RecordForm.CheckTime" :disabled="true"></el-input>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                                <el-row >
                                    <el-col :span='22'>
                                        <el-form-item label="检验依据：">
                                            <el-input v-model="RecordForm.Basis"></el-input>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                            </el-form>
                            <el-col class="mgt24">
                                <el-col :span='22'>
                                    <el-tag type="info">【鉴别】：</el-tag>
                                    <div class="mgt14">
                                        <div v-for="(item,index) in Discerns" :label="item" :key="index">
                                            <el-row class="mgb10">
                                                <el-col :span='18' class="fsz12 ">{{item.work}}</el-col>
                                                <el-col :span='3' class="fsz10 lightgreen">{{item.Name}}</el-col>
                                                <el-col :span='3'>
                                                   <el-checkbox v-model="item.Status" v-if="item.Name=='莫黄敏'">是否符合</el-checkbox>
                                                </el-col>
                                            </el-row>
                                        </div>
                                    </div>
                                </el-col>
                                <el-col :span='22' class="mgt24">
                                    <el-tag type="success">【检查】：</el-tag>
                                    <div class="mgt14">
                                        <div v-for="(item,index) in Inspects" :label="item" :key="index">
                                            <el-row class="mgb10">
                                                <el-col :span='18' class="fsz12 ">{{item.work}}</el-col>
                                                <el-col :span='3' class="fsz10 lightgreen">{{item.Name}}</el-col>
                                                <el-col :span='3'>
                                                   <el-checkbox v-model="item.Status" v-if="item.Name=='莫黄敏'">是否符合</el-checkbox>
                                                </el-col>
                                            </el-row>
                                        </div>
                                    </div>
                                </el-col>
                                <el-col :span='22' class="mgt24">
                                    <el-tag type="info">【微生物测定】：</el-tag>
                                    <div class="mgt14">
                                        <div v-for="(item,index) in Microbes" :label="item" :key="index">
                                            <el-row class="mgb10">
                                                <el-col :span='18' class="fsz12 ">{{item.work}}</el-col>
                                                <el-col :span='3' class="fsz10 lightgreen">{{item.Name}}</el-col>
                                                <el-col :span='3'>
                                                   <el-checkbox v-model="item.Status" v-if="item.Name=='莫黄敏'">是否符合</el-checkbox>
                                                </el-col>
                                            </el-row>
                                        </div>
                                    </div>
                                </el-col>
                                <el-col :span='22' class="mgt24">
                                    <el-tag type="danger">【性状】：</el-tag>
                                    <div class="mgt14">
                                        <div v-for="(item,index) in Characters" :label="item" :key="index">
                                            <el-row class="mgb10">
                                                <el-col :span='18' class="fsz12 ">{{item.work}}</el-col>
                                                <el-col :span='3' class="fsz10 lightgreen">{{item.Name}}</el-col>
                                                <el-col :span='3'>
                                                   <el-checkbox v-model="item.Status" v-if="item.Name=='莫黄敏'">是否符合</el-checkbox>
                                                </el-col>
                                            </el-row>
                                        </div>
                                    </div>
                                </el-col>
                                <el-col :span='22' class="mgt24">
                                    <el-tag type="info">【含量测定】：</el-tag>
                                    <div class="mgt14">
                                        <div v-for="(item,index) in Contents" :label="item" :key="index">
                                            <el-row class="mgb10">
                                                <el-col :span='18' class="fsz12 ">{{item.work}}</el-col>
                                                <el-col :span='3' class="fsz10 lightgreen">{{item.Name}}</el-col>
                                                <el-col :span='3'>
                                                   <el-checkbox v-model="item.Status" v-if="item.Name=='莫黄敏'">是否符合</el-checkbox>
                                                </el-col>
                                            </el-row>
                                        </div>
                                    </div>
                                </el-col>
                            </el-col>
                        </div>
                 </el-col>
                <el-col class="mgt24" style="textAlign:right;"><el-button type="primary" @click="postResult">发送结果</el-button></el-col>
            </el-row>
        </el-col>
    </el-row>
</template>
<script>
var moment=require('moment')
export default {
    data(){
        return {
           RecordForm:{ //检验记录清单
               Type:'',
               CheckTime:'',
               Basis:'',
           },
           opt:{
               Discernopt:true,
               Inspectopt:true,
               Characteropt:true,
               Contentopt:true,
               Microbeopt:true,
           },
           Row:{},
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
            Discerns:[],
            Inspects:[],
            Characters:[],
            Contents:[],
            Microbes:[],
            CheckProjectNO:'',
            batchtableconfig:[{prop:'CheckNumber',label:'请验单号'},{prop:'Name',label:'品名'},{prop:'CheckDate',label:'请验时间',width:155}],//批次列表
        }
    },
    created(){
       this.getSelectOption()
       this.SearchTab()
    },
    methods: {
        postResult(){ //发送结果按钮
            var arr1=this.Discerns.map((item, index) => {
                if(item.Name=='莫黄敏'){
                    return {Id:item.Id,Status:(item.Status).toString()}
                }
            })
            var arr2=this.Inspects.map((item, index) => {
                if(item.Name=='莫黄敏'){
                return {Id:item.Id,Status:(item.Status).toString()}
                }
            })
            var arr3=this.Characters.map((item, index) => {
                if(item.Name=='莫黄敏'){
                return {Id:item.Id,Status:(item.Status).toString()}
                }
            })
            var arr4=this.Contents.map((item, index) => {
                if(item.Name=='莫黄敏'){
                return {Id:item.Id,Status:(item.Status).toString()}
                }
            })
            var arr5=this.Microbes.map((item, index) => {
                if(item.Name=='莫黄敏'){
                return {Id:item.Id,Status:(item.Status).toString()}
                }
            })
            var arr=[...arr1,...arr2,...arr3,...arr4,...arr5]
            var params={
                CheckProjectNO:this.CheckProjectNO,
                Name:'莫黄敏',
                Action:JSON.stringify(arr),
                CheckEndTime:moment(new Date()).format('YYYY-MM-DD HH:mm:ss'),
            }
            this.axios.post('/lims/QualityTesting',this.qs.stringify(params)).then((res) => {
                console.log(res)
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
                Status:'质检'
            }
            this.axios.get('/lims/CheckForm',{params:params}).then((res) => {
                this.batchTableData.data=res.data.data
                this.batchTableData.total=res.data.total
            })
        },
        handletabClick(row){ //左侧tab点击事件
            this.CheckProjectNO=row.CheckProjectNO
            this.Row=row
            this.RecordForm.CheckTime=moment(new Date()).format('YYYY-MM-DD HH:mm:ss')
            this.getJbInfo(row.CheckProjectNO)
        },
        getJbInfo(CheckProjectNO){
            var params={
                CheckProjectNO:CheckProjectNO,
                Name:'莫黄敏'
            }
            this.axios.get('/lims/QualityTesting',{params:params}).then((res) => {
                var arr=res.data.data
                arr.forEach((item, index) => {
                    if(item.CheckType=='Microbe'){
                        this.Microbes=item.values
                    }
                    if(item.CheckType=='Discern'){
                        this.Discerns=item.values
                    }
                    if(item.CheckType=='Inspect'){
                        this.Inspects=item.values
                    }
                    if(item.CheckType=='Character'){
                        this.Characters=item.values
                    }
                    if(item.CheckType=='Content'){
                        this.Contents=item.values
                    }
                })
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
     .jbcontent{
         height:30px;
         line-height:30px;
     }
</style>
