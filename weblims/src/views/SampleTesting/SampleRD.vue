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
                        <el-col :span='6' class="req mgl15" style="paddingTop:3px;">
                             <el-radio-group v-model="radio2"  @change='selectSampleTab'>
                                <el-radio-button label="样本分发" ></el-radio-button>
                                <el-radio-button label="记录分发"></el-radio-button>
                             </el-radio-group>
                        </el-col>
                    </el-row>
                </el-col>
                <el-col :span='24'>
                      <el-row class="padd15" v-if="radio2=='样本分发'">
                          <el-col :span='24' class="container mgt24" style="backgroundColor:#EAEAEA;">
                              <el-col :span='20'>
                                  <el-col :span='24' class="lightgreen fsz20"><el-checkbox label="去检验" @change="isDiscern" checked></el-checkbox></el-col>
                                  <el-col :span='24' class="mgt24">
                                      <el-row :gutter='10'>
                                          <el-col :span='5'>样品品名</el-col>
                                          <el-col :span='4'>类别</el-col>
                                          <el-col :span='5'>批号(物料代码)</el-col>
                                          <el-col :span='5'>分配样量</el-col>
                                          <el-col :span='5'>编号</el-col>
                                      </el-row>
                                  </el-col>
                                  <el-col :span='24' class="mgt24">
                                       <el-row :gutter='10'>
                                          <el-col :span='5' class="lightgreen padt8">{{Row.Name}}</el-col>
                                          <el-col :span='4' class="lightgreen padt8">{{Row.ProductType}}</el-col>
                                          <el-col :span='5' class="lightgreen padt8">{{Row.Number}}</el-col>
                                          <el-col :span='5'>
                                              <el-input placeholder="请输入内容" v-model="distribute.Account1" clearable></el-input>
                                          </el-col>
                                          <el-col :span='5'>
                                              <el-input placeholder="请输入内容" v-model="distribute.no1" clearable></el-input>
                                          </el-col>
                                      </el-row>
                                  </el-col>
                              </el-col>
                              <el-col :span='4'>
                                  <el-col class="padtop50 padl40"><el-button type="success" @click="DistributeSample('J')">{{curSta}}</el-button></el-col>
                              </el-col>
                          </el-col>
                          <el-col :span='24' class="container mgt24" style="backgroundColor:#EAEAEA;">
                              <el-col :span='20'>
                                  <el-col :span='24' class="lightgreen fsz20"><el-checkbox label="去复查/备用"  :checked='Checkopt' @change="isCheck"></el-checkbox></el-col>
                                  <el-col :span='24' class="mgt24">
                                      <el-row :gutter='10'>
                                          <el-col :span='5'>样品品名</el-col>
                                          <el-col :span='4'>类别</el-col>
                                          <el-col :span='5'>批号(物料代码)</el-col>
                                          <el-col :span='5'>分配样量</el-col>
                                          <el-col :span='5'>编号</el-col>
                                      </el-row>
                                  </el-col>
                                  <el-col :span='24' class="mgt24">
                                        <el-row :gutter='10'>
                                          <el-col :span='5' class="lightgreen padt8">{{Row.Name}}</el-col>
                                          <el-col :span='4' class="lightgreen padt8">{{Row.ProductType}}</el-col>
                                          <el-col :span='5' class="lightgreen padt8">{{Row.Number}}</el-col>
                                          <el-col :span='5'>
                                              <el-input placeholder="请输入内容" v-model="distribute.Account2" clearable></el-input>
                                          </el-col>
                                          <el-col :span='5'>
                                              <el-input placeholder="请输入内容" v-model="distribute.no2" clearable></el-input>
                                          </el-col>
                                      </el-row>
                                  </el-col>
                              </el-col>
                              <el-col :span='4'>
                                    <el-col class="padtop50 padl40"><el-button type="success">确认分发</el-button></el-col>
                              </el-col>
                          </el-col>
                          <el-col :span='24' class="container mgt24" style="backgroundColor:#EAEAEA;">
                              <el-col :span='20'>
                                  <el-col :span='24' class="lightgreen fsz20"><el-checkbox label="去留样" :checked='Lyopt' @change="isLy"></el-checkbox></el-col>
                                  <el-col :span='24' class="mgt24">
                                      <el-row :gutter='10'>
                                          <el-col :span='5'>样品品名</el-col>
                                          <el-col :span='4'>类别</el-col>
                                          <el-col :span='5'>批号(物料代码)</el-col>
                                          <el-col :span='5'>分配样量</el-col>
                                          <el-col :span='5'>编号</el-col>
                                      </el-row>
                                  </el-col>
                                  <el-col :span='24' class="mgt24">
                                       <el-row :gutter='10'>
                                          <el-col :span='5' class="lightgreen padt8">{{Row.Name}}</el-col>
                                          <el-col :span='4' class="lightgreen padt8">{{Row.ProductType}}</el-col>
                                          <el-col :span='5' class="lightgreen padt8">{{Row.Number}}</el-col>
                                          <el-col :span='5'>
                                              <el-input placeholder="请输入内容" v-model="distribute.Account3" clearable></el-input>
                                          </el-col>
                                          <el-col :span='5'>
                                              <el-input placeholder="请输入内容" v-model="distribute.no3" clearable></el-input>
                                          </el-col>
                                      </el-row>
                                  </el-col>
                              </el-col>
                              <el-col :span='4'>
                                  <el-col class="padtop50 padl40"><el-button type="success" @click="DistributeSample('L')">{{curSta}}</el-button></el-col>
                              </el-col>
                          </el-col>
                      </el-row>
                </el-col>
                 <el-col class="mgt24" style="textAlign:right;" v-if="radio2=='样本分发'"><el-button :type="(Discernopt || Checkopt || Lyopt)?'primary':'info'" @click="mulDistribute">确认分发</el-button></el-col>
            </el-row>
            <el-row v-if="radio2=='记录分发'" class="mgt24">
                 <el-col :span='24' class="container">
                    <el-menu :default-active="'1'" class="bgwhite mgt24" mode="horizontal" @select="handleSelect">
                        <el-menu-item :index="'1'" style="height:46px;lineHeight:30px;" v-if="Discernopt">检验记录</el-menu-item>
                        <el-menu-item :index="'2'"  style="height:46px;lineHeight:30px;" v-if="Lyopt">留样记录</el-menu-item>
                        <el-menu-item :index="'3'"  style="height:46px;lineHeight:30px;" v-if="Checkopt">复查记录</el-menu-item>
                    </el-menu>
                    <div v-if="currentChoose=='1'">
                        <div class="mgt24 mgb24">产品检验原始记录</div>
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
                            <el-form >
                                <el-col :span='22'>
                                    <el-tag type="info">【鉴别】：</el-tag>
                                    <p v-for="(item,index) in Discerns" :key='index' class="lightgreen jbcontent fsz10">{{item.value}}</p>
                                    <el-divider></el-divider>
                                </el-col>
                                <el-col :span='22'>
                                    <el-tag type="success">【检查】：</el-tag>
                                    <p v-for="(item,index) in Inspects" :key='index' class="lightgreen jbcontent fsz10">{{item.value}}</p>
                                    <el-divider></el-divider>
                                </el-col>
                                <el-col :span='22'>
                                    <el-tag type="warning">【性状】：</el-tag>
                                    <p v-for="(item,index) in Characters" :key='index' class="lightgreen jbcontent fsz10">{{item.value}}</p>
                                    <el-divider></el-divider>
                                </el-col>
                                <el-col :span='22'>
                                    <el-tag type="danger">【含量测定】：</el-tag>
                                    <p v-for="(item,index) in Contents" :key='index'  class="lightgreen jbcontent fsz10">{{item.value}}</p>
                                    <el-divider></el-divider>
                                </el-col>
                                <el-col :span='22'>
                                    <el-tag type="info">【微生物限度】：</el-tag>
                                    <p v-for="(item,index) in Microbes" :key='index'  class="lightgreen jbcontent fsz10">{{item.value}}</p>
                                </el-col>
                            </el-form>
                            </el-col>
                        </div>
                    </div>
                    <div v-if="currentChoose=='2'">
                        <div class="mgt24 mgb24">产品留样原始记录</div>
                        <div style="border:1px solid #ccc;paddingTop:26px;">
                            <el-form ref="form" :model="LyForm" label-width="100px">
                                <el-row>
                                    <el-col :span='11'>
                                        <el-form-item label="品名：">
                                            <el-input v-model="Row.Name" :disabled="true"></el-input>
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
                                            <el-input v-model="LyForm.PackSpecs"></el-input>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                                <el-row >
                                    <el-col :span='11'>
                                        <el-form-item label="理论产量：">
                                            <el-input v-model="LyForm.TheoreticalYield"></el-input>
                                        </el-form-item>
                                    </el-col>
                                    <el-col :span='11'>
                                        <el-form-item label="留样数量：">
                                            <el-input v-model="LyForm.BatchAmount"></el-input>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                                <el-row >
                                    <el-col :span='11'>
                                        <el-form-item label="留样部门：">
                                            <el-input v-model="LyForm.BatchDepartment"></el-input>
                                        </el-form-item>
                                    </el-col>
                                    <el-col :span='11'>
                                        <el-form-item label="留样人：">
                                            <el-input v-model="LyForm.BatchName"></el-input>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                                <el-row >
                                    <el-col :span='11'>
                                        <el-form-item label="留样位置：">
                                            <el-input v-model="LyForm.Position"></el-input>
                                        </el-form-item>
                                    </el-col>
                                    <el-col :span='11'>
                                        <el-form-item label="留样时间：">
                                            <el-date-picker v-model="LyForm.BatchTime" type="date" placeholder="选择日期"></el-date-picker>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                                <el-row >
                                    <el-col :span='11'>
                                        <el-form-item label="经手人：">
                                            <el-input v-model="LyForm.Handler"></el-input>
                                        </el-form-item>
                                    </el-col>
                                    <el-col :span='11'>
                                        <el-form-item label="生产日期：">
                                            <el-date-picker v-model="LyForm.ProductionDate" type="date" placeholder="选择日期"></el-date-picker>
                                        </el-form-item>
                                    </el-col>
                                </el-row>  
                                <el-row >
                                    <el-col :span='11'>
                                        <el-form-item label="有效日期：">
                                            <el-date-picker v-model="LyForm.ValidityDate" type="date" placeholder="选择日期"></el-date-picker>
                                        </el-form-item>
                                    </el-col>
                                    <el-col :span='11'>
                                        <el-form-item label="备注：">
                                            <el-input type="textarea" autosize placeholder="请输入内容" v-model="LyForm.Comment"></el-input>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                            </el-form>
                        </div>
                    </div>
                    <div v-if="currentChoose=='3'">
                        <div class="mgt24 mgb24">产品复查原始记录</div>
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
                        </div>
                    </div>
                 </el-col>
                <el-col class="mgt24" style="textAlign:right;" v-if="radio2=='记录分发'"><el-button type="primary" @click="postSampleRecord" >确认分发</el-button></el-col>
            </el-row>
        </el-col>
    </el-row>
</template>
<script>
var moment=require('moment')
export default {
    data(){
        return {
           curSta:'确认分发',
           Discernopt:true,
           Checkopt:false,
           Lyopt:false,
           RecordForm:{
               Type:'',
               CheckTime:'',
               Basis:'',
           },
           LyForm:{
               PackSpecs:'',
               TheoreticalYield:'',
               BatchAmount:'',
               BatchDepartment:'',
               BatchName:'',
               Position:'',
               BatchTime:'',
               Handler:'',
               ProductionDate:'',
               ValidityDate:'',
               Comment:''
           },
           Row:{},
           distribute:{
               no1:'',
               Account1:'',
               no2:'',
               Account2:'',
               no3:'',
               Account3:'',
               CheckProjectNO:'',

           },
           currentChoose:'2',
           radio2:'样本分发',
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
            batchtableconfig:[{prop:'CheckNumber',label:'请验单号'},{prop:'Name',label:'品名'},{prop:'CheckDate',label:'请验时间',width:155}],//批次列表
        }
    },
    created(){
       this.getSelectOption()
       this.getInitTab()
    },
    methods: {
        mulDistribute(){
            var params={
                 Time:moment(new Date()).format('YYYY-MM-DD HH:mm:ss'),
                 CheckProjectNO:this.distribute.CheckProjectNO,
                 User:localStorage.getItem('Name'),
                 CheckProjectNO:this.distribute.CheckProjectNO,
            }
            if(!this.Discernopt && !this.Checkopt && !this.Lyopt){
                this.$message({
                    type:'warning',
                    message:'请先勾选要分发的内容'
                })
            }else if(this.Discernopt){
                if(this.Checkopt){
                    if(this.Lyopt){
                        params.Account=JSON.stringify([this.distribute.Account1,this.distribute.Account2,this.distribute.Account3]),
                        params.no=JSON.stringify([this.distribute.no1,this.distribute.no2,this.distribute.no3]),
                        params.Action=JSON.stringify(['J','F','L'])
                        }else{
                        params.Account=JSON.stringify([this.distribute.Account1,this.distribute.Account2]),
                        params.no=JSON.stringify([this.distribute.no1,this.distribute.no2]),
                        params.Action=JSON.stringify(['J','F'])
                        }
                    }else{
                       if(this.Lyopt){
                        params.Account=JSON.stringify([this.distribute.Account1,this.distribute.Account3]),
                        params.no=JSON.stringify([this.distribute.no1,this.distribute.no3]),
                        params.Action=JSON.stringify(['J','L'])
                        }else{
                        params.Account=JSON.stringify([this.distribute.Account1]),
                        params.no=JSON.stringify([this.distribute.no1]),
                        params.Action=JSON.stringify(['J'])
                        }
                    }
                }else{
                    if(this.Checkopt){
                    if(this.Lyopt){
                        params.Account=JSON.stringify([this.distribute.Account2,this.distribute.Account3]),
                        params.no=JSON.stringify([this.distribute.no2,this.distribute.no3]),
                        params.Action=JSON.stringify(['F','L'])
                        }else{
                        params.Account=JSON.stringify([this.distribute.Account2]),
                        params.no=JSON.stringify([this.distribute.no2]),
                        params.Action=JSON.stringify(['F'])
                        }
                    }else{
                       if(this.Lyopt){
                        params.Account=JSON.stringify([this.distribute.Account3]),
                        params.no=JSON.stringify([this.distribute.no3]),
                        params.Action=JSON.stringify(['L'])
                        }else{
                         return false;
                        }
                    }
                }
            this.axios.post('/lims/Distribute',this.qs.stringify(params)).then((res) => {
               if(res.data.code=='1000'){
                   this.$message({
                       type:'success',
                       message:'分发成功'
                   })
                   this.curSta='已分发'
               }else{
                   this.$message({
                       type:'info',
                       message:'请重试'
                   })
               }
           })

        },
        postSampleRecord(){ //记录分发
            var params1={
                CheckProjectNO:this.distribute.CheckProjectNO,
                Type:this.RecordForm.Type,
                CheckTime:this.RecordForm.CheckTime,
                Basis:this.RecordForm.Basis,
            }
            var params2={
               CheckProjectNO:this.distribute.CheckProjectNO,
               Product:this.Row.Name,
               Specs:this.Row.Specs,
               ProductNumber:this.Row.ProductNumber,
               PackSpecs:this.LyForm.PackSpecs,
               TheoreticalYield:this.LyForm.TheoreticalYield,
               BatchAmount:this.LyForm.BatchAmount,
               BatchDepartment:this.LyForm.BatchDepartment,
               BatchName:this.LyForm.BatchName,
               Position:this.LyForm.Position,
               BatchTime:moment(this.LyForm.BatchTime).format("YYYY-MM-DD"),
               Handler:this.LyForm.Handler,
               ProductionDate:moment(this.LyForm.ProductionDate).format("YYYY-MM-DD"),
               ValidityDate:moment(this.LyForm.ValidityDate).format("YYYY-MM-DD"),
               Comment:this.LyForm.Comment
            }
            if(this.currentChoose=='1'){
                this.axios.post('/lims/CheckRecord',this.qs.stringify(params1)).then((res) => {
                if(res.data.code=='1000'){
                    this.$message({
                        type:'success',
                        message:'检验记录下发成功'
                    })
                }else{
                    this.$message({
                        type:'error',
                        message:'检验记录下发失败'
                    })
                }
            })
            }else if(this.currentChoose=='2'){
                this.axios.post('/lims/ProductSave',this.qs.stringify(params2)).then((res) => {
                if(res.data.code=='1000'){
                    this.$message({
                        type:'success',
                        message:'留样记录下发成功'
                    })
                }else{
                    this.$message({
                        type:'error',
                        message:'留样记录下发失败'
                    })
                }
            })
            }
           
        },
        DistributeSample(act){
            var params={
                 Time:moment(new Date()).format('YYYY-MM-DD HH:mm:ss'),
                 CheckProjectNO:this.distribute.CheckProjectNO,
                 User:localStorage.getItem('Name'),
                 CheckProjectNO:this.distribute.CheckProjectNO,
            }
            if(act=='J'){
                params.Account=JSON.stringify([this.distribute.Account1]),
                params.no=JSON.stringify([this.distribute.no1]),
                params.Action=JSON.stringify(['J'])
            }else if(act=='L'){
                params.Account=JSON.stringify([this.distribute.Account3]),
                params.no=JSON.stringify([this.distribute.no3]),
                params.Action=JSON.stringify(['L'])
            }else if(act=='F'){
                params.Account=JSON.stringify([this.distribute.Account2]),
                params.no=JSON.stringify([this.distribute.no2]),
                params.Action=JSON.stringify(['F'])
            }
           this.axios.post('/lims/Distribute',this.qs.stringify(params)).then((res) => {
               if(res.data.code=='1000'){
                   this.$message({
                       type:'success',
                       message:'分发成功'
                   })
                   this.curSta='已分发'
               }else{
                   this.$message({
                       type:'info',
                       message:'请重试'
                   })
               }
           })
        },
        isDiscern(e){ //是否检验
            if(e){
                this.Discernopt=true
            }else{
                this.Discernopt=false
            }
        },
        isCheck(e){ //是否复查
            if(e){
                this.Checkopt=true
            }else{
                this.Checkopt=false
            }
        },
        isLy(e){ //是否留样
            if(e){
                this.Lyopt=true
            }else{
                this.Lyopt=false
            }
        },
        handleSelect(key) {
            this.currentChoose=key
        },
        selectSampleTab(e){
            this.radio2=e
            if(e==='记录分发'){
                this.currentChoose='1'
            }
        },
        LookJbInfo(){
            this.dialogTableVisible=true
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
                Status:'分发'
            }
            this.axios.get('/lims/CheckForm',{params:params}).then((res) => {
                this.batchTableData.data=res.data.data
                this.batchTableData.total=res.data.total
            })
        },
         getInitTab(){ //初始化获取表格数据
            var params={
                Page:this.batchTableData.offset,
                PerPage:this.batchTableData.limit,
                Product:this.searchObj.category,
                DateTime:this.searchObj.registrydate,
                Status:'分发'
            }
            this.axios.get('/lims/CheckForm',{params:params}).then((res) => {
                this.batchTableData.data=res.data.data
                this.batchTableData.total=res.data.total
            })
        },
        handletabClick(row){ //左侧tab点击事件
            this.curSta='确认分发'
            this.Row=row
            this.RecordForm.CheckTime=moment(new Date()).format('YYYY-MM-DD HH:mm:ss')
            this.distribute.CheckProjectNO=row.CheckProjectNO
            this.getJbInfo(row.CheckProjectNO)
        },
        getJbInfo(CheckProjectNO){
            var params={
                CheckProjectNO:CheckProjectNO
            }
            this.axios.get('/lims/Sample',{params:params}).then((res) => {
                this.Discerns=res.data.data[0].Discern
                this.Inspects=res.data.data[0].Inspect
                this.Characters=res.data.data[0].Character
                this.Contents=res.data.data[0].Content
                this.Characters=res.data.data[0].Character
                this.Microbes=res.data.data[0].Microbe
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
