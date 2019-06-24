using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using QK365.Component.Data;
namespace QK365.Core.DB.EntityModel
{
    ///<summary>
    /// The entity class for DB table project_acceptance_list .
    ///</summary>
    [Table("project_acceptance_list")]
    public class ProjectAcceptanceListEntity
    {
        ///<summary>
        /// 自增主键
        ///</summary>
        [Column("id")]
        public System.Int64 Id { get; set; }
        
        ///<summary>
        /// FK,acceptance_list
        ///</summary>
        [Column("acceptance_list_id")]
        public System.Int32 AcceptanceListId { get; set; }
        
        ///<summary>
        /// 单号，生成规则yyyyMMddHHmmss0001
        ///</summary>
        [Column("code")]
        public System.String Code { get; set; }
        
        ///<summary>
        /// FK,工程装修ID
        ///</summary>
        [Column("project_id")]
        public System.Int32 ProjectId { get; set; }
        
        ///<summary>
        /// FK,单元ID
        ///</summary>
        [Column("cuc_id")]
        public System.Int32 CucId { get; set; }
        
        ///<summary>
        /// 状态：0：单子开具中1：单子开具完成2：单子已经失效
        ///</summary>
        [Column("status")]
        public System.Int32 Status { get; set; }
        
        ///<summary>
        /// 验收员意见1：通过0：不通过
        ///</summary>
        [Column("inspector_opinion")]
        public System.Int32 InspectorOpinion { get; set; }
        
        ///<summary>
        /// 验收员备注
        ///</summary>
        [Column("inspector_desc")]
        public System.String InspectorDesc { get; set; }
        
        ///<summary>
        /// 验收时间
        ///</summary>
        [Column("inspector_time")]
        public System.DateTime InspectorTime { get; set; }
        
        ///<summary>
        /// FK, 验收员ID
        ///</summary>
        [Column("inspector_operator_id")]
        public System.Int32 InspectorOperatorId { get; set; }
        
        ///<summary>
        /// 验收员验收设备的IMEI
        ///</summary>
        [Column("inspector_imei")]
        public System.String InspectorImei { get; set; }
        
        ///<summary>
        /// 验收员验收设备的IP
        ///</summary>
        [Column("inspector_ip")]
        public System.String InspectorIp { get; set; }
        
        ///<summary>
        /// 市场部门对验收单的意见1：合格的验收单0：验收单不合格，需重新验收
        ///</summary>
        [Column("market_opinion")]
        public System.Int32 MarketOpinion { get; set; }
        
        ///<summary>
        /// 市场部门备注
        ///</summary>
        [Column("market_desc")]
        public System.String MarketDesc { get; set; }
        
        ///<summary>
        /// 市场部门审核时间
        ///</summary>
        [Column("market_time")]
        public System.DateTime MarketTime { get; set; }
        
        ///<summary>
        /// FK, 市场部门操作人员ID
        ///</summary>
        [Column("market_operator_id")]
        public System.Int32 MarketOperatorId { get; set; }
        
        ///<summary>
        /// 工程部门对罚单的意见1：罚单通过，且整改完成0：罚单不合理
        ///</summary>
        [Column("engineering_opinion")]
        public System.Int32 EngineeringOpinion { get; set; }
        
        ///<summary>
        /// 工程部门备注
        ///</summary>
        [Column("engineering_desc")]
        public System.String EngineeringDesc { get; set; }
        
        ///<summary>
        /// 工程部门审核时间
        ///</summary>
        [Column("engineering_time")]
        public System.DateTime EngineeringTime { get; set; }
        
        ///<summary>
        /// FK, 工程部门操作人员ID
        ///</summary>
        [Column("engineering_operator_id")]
        public System.Int32 EngineeringOperatorId { get; set; }
        
        ///<summary>
        /// 市场部门对工程部审核的意见1：审核通过0：审核不通过，需重新整改
        ///</summary>
        [Column("market_engineering_opinion")]
        public System.Int32 MarketEngineeringOpinion { get; set; }
        
        ///<summary>
        /// 市场部门对工程部审核的审核时间
        ///</summary>
        [Column("market_engineering_desc")]
        public System.String MarketEngineeringDesc { get; set; }
        
        ///<summary>
        /// 市场部门对工程部审核的审核时间 
        ///</summary>
        [Column("market_engineering_time")]
        public System.DateTime MarketEngineeringTime { get; set; }
        
        ///<summary>
        /// FK, 市场部门操作人员ID
        ///</summary>
        [Column("market_engineering_operator_id")]
        public System.Int32 MarketEngineeringOperatorId { get; set; }
        
        ///<summary>
        /// 服务中心的意见1：审核通过转待租其它：按照流程转整改待验收
        ///</summary>
        [Column("service_centre_opinion")]
        public System.Int32 ServiceCentreOpinion { get; set; }
        
        ///<summary>
        /// 服务中心审核的备注
        ///</summary>
        [Column("service_centre_desc")]
        public System.String ServiceCentreDesc { get; set; }
        
        ///<summary>
        /// 服务中心的审核时间
        ///</summary>
        [Column("service_centre_time")]
        public System.DateTime ServiceCentreTime { get; set; }
        
        ///<summary>
        /// FK, 服务中心操作人员ID
        ///</summary>
        [Column("service_centre_operator_id")]
        public System.Int32 ServiceCentreOperatorId { get; set; }
        
        ///<summary>
        /// 网络资源合格说明:1-无资源 2-已安装 3-特殊情况
        ///</summary>
        [Column("network_resource")]
        public System.Int32 NetworkResource { get; set; }
        
        ///<summary>
        /// 工程图纸url地址
        ///</summary>
        [Column("drawings_url")]
        public System.String DrawingsUrl { get; set; }
        
        ///<summary>
        /// 不合格说明项名称，逗号分隔
        ///</summary>
        [Column("unqualified_titles")]
        public System.String UnqualifiedTitles { get; set; }
        
        ///<summary>
        /// 不合格说明项id列表
        ///</summary>
        [Column("unqualified_ids")]
        public System.String UnqualifiedIds { get; set; }
        
        ///<summary>
        /// 最后一次整改完成时间
        ///</summary>
        [Column("last_reform_finish_time")]
        public System.DateTime LastReformFinishTime { get; set; }
        
        ///<summary>
        /// 时间戳
        ///</summary>
        [Column("ts")]
        public System.Int64 Ts { get; set; }
        
        ///<summary>
        /// 从原表同步到报表的时间
        ///</summary>
        [Column("sync_time")]
        public System.DateTime SyncTime { get; set; }
        
        ///<summary>
        /// 最后更新时间
        ///</summary>
        [Column("modify_time")]
        public System.DateTime ModifyTime { get; set; }
        
    }
}
