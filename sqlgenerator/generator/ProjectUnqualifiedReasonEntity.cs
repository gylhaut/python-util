using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using QK365.Component.Data;
namespace QK365.Core.DB.EntityModel
{
    ///<summary>
    /// The entity class for DB table project_unqualified_reason .
    ///</summary>
    [Table("project_unqualified_reason")]
    public class ProjectUnqualifiedReasonEntity
    {
        ///<summary>
        /// 自增主键
        ///</summary>
        [Column("id")]
        public System.Int64 Id { get; set; }
        
        ///<summary>
        /// FK,unqualified_reason
        ///</summary>
        [Column("unqualified_id")]
        public System.Int32 UnqualifiedId { get; set; }
        
        ///<summary>
        /// 
        ///</summary>
        [Column("unqualified_code")]
        public System.String UnqualifiedCode { get; set; }
        
        ///<summary>
        /// 
        ///</summary>
        [Column("unqualified_title")]
        public System.String UnqualifiedTitle { get; set; }
        
        ///<summary>
        /// 时间戳
        ///</summary>
        [Column("ts")]
        public System.Int64 Ts { get; set; }
        
        ///<summary>
        /// 
        ///</summary>
        [Column("is_delete")]
        public System.Boolean IsDelete { get; set; }
        
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
