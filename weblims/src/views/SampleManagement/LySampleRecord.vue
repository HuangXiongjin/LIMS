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
                     <div class="mgt24">成品留样记录表</div>
                     <el-divider></el-divider>
                     <el-row style="paddingTop:10px;">
                         <el-col :span='2'>品名：</el-col>
                         <el-col :span='3' class="lightgreen">{{Row.Name}}</el-col>
                         <el-col :span='2'>温度：</el-col>
                         <el-col :span='2' class="lightgreen">25</el-col>
                         <el-col :span='3'>相对湿度：</el-col>
                         <el-col :span='3' class="lightgreen">xxx</el-col>
                         <el-col :span='3'>留样位置：</el-col>
                         <el-col :span='3' class="lightgreen">{{Row.Position}}</el-col>
                         <el-col :span='3' class="lightgreen">{{Row.ProductNumber}}</el-col>
                     </el-row>
                     <el-row style="paddingTop:26px;height:400px;">
                         <el-table :data="[Row]" style="width: 100%">
                            <el-table-column prop="ProductNumber" label="留样批号"></el-table-column>
                            <el-table-column prop="BatchTime" label="留样日期" width="150"></el-table-column>
                            <el-table-column prop="Specs" label="规格"></el-table-column>
                            <el-table-column prop="BatchAmount" label="留样量"></el-table-column>
                            <el-table-column prop="Handler" label="经手人"></el-table-column>
                            <el-table-column prop="ProductNumber" label="观察项目"></el-table-column>
                            <el-table-column label="观察结果及操作人">
                            <el-table-column
                                prop="name"
                                label="6个月"
                                >
                            </el-table-column>
                            <el-table-column
                                prop="name"
                                label="12个月"
                                >
                            </el-table-column>
                            <el-table-column
                                prop="name"
                                label="18个月"
                                >
                            </el-table-column>
                            <el-table-column
                                prop="name"
                                label="24个月"
                                >
                            </el-table-column>
                            <el-table-column
                                prop="name"
                                label="30个月"
                                >
                            </el-table-column>
                            <el-table-column
                                prop="name"
                                label="36个月"
                                >
                            </el-table-column>
                            <el-table-column
                                prop="name"
                                label="48个月"
                                >
                            </el-table-column>
                            </el-table-column>
                            <el-table-column prop="date" label="结论"></el-table-column>
                            <el-table-column prop="Comment" label="备注"></el-table-column>
                         </el-table>

                     </el-row>
                </el-col>
            </el-row>
            <el-col class="mgt24" style="textAlign:right;">
                <el-button type="primary" :disabled='xfopt'>编辑</el-button>
                <el-button type="success" :disabled='xfopt'>保存</el-button>
                <el-button type="danger" :disabled='xfopt' @click="requireDestroy">申请销毁</el-button>
            </el-col>
        </el-col>
    </el-row>
</template>
<script>
var moment=require('moment')
export default {
    data(){
        return {
            batchTableData:{ //物料BOM
                data:[],
                limit: 5,//当前显示多少条
                offset: 1,//当前处于多少页
                total: 0,//总的多少页
            },
           Row:{},
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
            batchtableconfig:[{prop:'ProductNumber',label:'产品批号'},{prop:'Name',label:'品名'},{prop:'BatchTime',label:'留样时间',width:155}],//批次列表
        }
    },
    created(){
       this.getSelectOption()
       this.SearchTab()
    },
    methods: {
         requireDestroy(){ //申请销户
            var params={
                CheckProjectNO:Row.CheckProjectNO,
                DestructionType:'留样销毁'
            }
            this.axios.post('/lims/Destruction',this.qs.stringify(params)).then((res) => {
                if(res.data.code=='1000'){
                    this.$message({
                        type:'success',
                        message:'申请销毁成功'
                    })
                }else{
                     this.$message({
                        type:'info',
                        message:'申请失败，请重试'
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