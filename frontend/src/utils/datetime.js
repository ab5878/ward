import { format, formatDistanceToNow } from 'date-fns';
import { toZonedTime } from 'date-fns-tz';

const IST_TIMEZONE = 'Asia/Kolkata';

/**
 * Convert UTC date to IST and format
 * @param {string|Date} date - UTC date
 * @param {string} formatStr - date-fns format string
 * @returns {string} Formatted IST date
 */
export const toIST = (date, formatStr = 'dd MMM, HH:mm') => {
  if (!date) return '';
  try {
    const utcDate = typeof date === 'string' ? new Date(date) : date;
    const istDate = utcToZonedTime(utcDate, IST_TIMEZONE);
    return `${format(istDate, formatStr)} IST`;
  } catch (error) {
    console.error('Date formatting error:', error);
    return '';
  }
};

/**
 * Format date for display (day, date, time in IST)
 * @param {string|Date} date
 * @returns {string}
 */
export const formatISTFull = (date) => {
  return toIST(date, 'EEE, dd MMM yyyy, HH:mm');
};

/**
 * Format date as relative time ("2 hours ago")
 * @param {string|Date} date
 * @returns {string}
 */
export const formatRelative = (date) => {
  if (!date) return '';
  try {
    const utcDate = typeof date === 'string' ? new Date(date) : date;
    return formatDistanceToNow(utcDate, { addSuffix: true });
  } catch (error) {
    console.error('Relative date formatting error:', error);
    return '';
  }
};

/**
 * Format time only in IST
 * @param {string|Date} date
 * @returns {string}
 */
export const formatTimeIST = (date) => {
  return toIST(date, 'HH:mm');
};

/**
 * Format date only in IST
 * @param {string|Date} date
 * @returns {string}
 */
export const formatDateIST = (date) => {
  return toIST(date, 'dd MMM yyyy');
};

/**
 * Get day label for timeline grouping
 * @param {string|Date} date
 * @returns {string}
 */
export const getDayLabel = (date) => {
  if (!date) return '';
  try {
    const utcDate = typeof date === 'string' ? new Date(date) : date;
    const istDate = utcToZonedTime(utcDate, IST_TIMEZONE);
    const today = utcToZonedTime(new Date(), IST_TIMEZONE);
    
    // Check if same day
    if (format(istDate, 'yyyy-MM-dd') === format(today, 'yyyy-MM-dd')) {
      return 'Today';
    }
    
    // Check if yesterday
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);
    if (format(istDate, 'yyyy-MM-dd') === format(yesterday, 'yyyy-MM-dd')) {
      return 'Yesterday';
    }
    
    return format(istDate, 'EEE, dd MMM yyyy');
  } catch (error) {
    console.error('Day label formatting error:', error);
    return '';
  }
};
